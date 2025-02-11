import atexit
import logging
import sys
from copy import copy
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Iterable, List, Mapping, Optional, Type, Union

from linkml_runtime import SchemaView
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot
from pydantic import BaseModel

from oaklib import BasicOntologyInterface
from oaklib.datamodels.obograph import Node
from oaklib.datamodels.settings import Settings
from oaklib.types import CURIE
from oaklib.utilities.iterator_utils import chunk

ID_KEY = "id"
LABEL_KEY = "label"


@dataclass
class StreamingWriter:
    """
    Base class for streaming writers.
    """

    file: Any = field(default_factory=lambda: sys.stdout)
    ontology_interface: BasicOntologyInterface = None
    display_options: List[str] = None
    autolabel: bool = None
    schemaview: Optional[SchemaView] = None
    index_slot: Optional[str] = None
    uses_schemaview = False
    list_delimiter: ClassVar[str] = None
    heterogeneous_keys: bool = False
    _output: Any = None
    object_count: int = field(default=0)
    settings: Settings = field(default_factory=lambda: Settings())
    primary_key: str = field(default="id")
    primary_value_field: str = field(default="label")
    pivot_fields: List[str] = field(default_factory=lambda: [])

    def __post_init__(self):
        atexit.register(self.close)

    def __hash__(self):
        return hash(str(self))

    @property
    def output(self) -> str:
        return self._output

    @output.setter
    def output(self, value) -> None:
        """
        Sets the output stream

        :param value:
        :return:
        """
        self._output = value
        if self._output is not None:
            if isinstance(self._output, str):
                self.file = open(self._output, "w", encoding="UTF-8")
            else:
                self.file = self._output

    def emit(
        self, obj: Union[YAMLRoot, BaseModel, dict, CURIE], label_fields: Optional[List[str]] = None
    ):
        """
        Emit an object or CURIE

        :param obj:
        :param label_fields:
        :return:
        """
        if isinstance(obj, CURIE):
            self.emit_curie(obj)
        elif isinstance(obj, Node):
            self.emit_curie(obj.id)
        elif isinstance(obj, BaseModel):
            self.emit_obj(obj)
        elif isinstance(obj, dict):
            self.emit_curie(obj[ID_KEY], obj.get(LABEL_KEY, None))
        else:
            self.emit_obj(obj)

    def emit_multiple(self, entities: Iterable[CURIE], **kwargs):
        """
        Emit multiple objects.

        :param entities:
        :param kwargs:
        :return:
        """
        for curie_it in chunk(entities):
            logging.info("** Next chunk:")
            for curie, label in self.ontology_interface.labels(
                curie_it, lang=self.settings.preferred_language
            ):
                self.emit(curie, label)

    def emit_curie(self, curie: CURIE, label=None):
        raise NotImplementedError

    def emit_obj(self, obj: Union[YAMLRoot, BaseModel]):
        obj_as_dict = json_dumper.to_dict(obj)
        return self.emit(obj_as_dict)

    def close(self):  # noqa
        pass

    def finish(self):
        # always ensure a file is writer
        self.file.write("")

    def line(self, v: str):
        self.file.write(f"{v}\n")

    def add_labels(self, obj_as_dict: Dict, label_fields: Optional[List[str]] = None) -> Dict:
        """
        Adds labels to the object

        :param obj_as_dict:
        :param label_fields:
        :return:
        """

        def _label(c: CURIE) -> str:
            lbl = self.ontology_interface.label(c, lang=self.settings.preferred_language)
            return str(lbl) if lbl else ""

        if label_fields and self.autolabel:
            for f in label_fields:
                curie = obj_as_dict.get(f, None)
                col_name = f"{f}_label"
                if curie and obj_as_dict.get(col_name, None) is None:
                    # allow for a list of CURIEs flattened using a delimiter
                    delim = self.list_delimiter
                    if delim and isinstance(curie, str) and delim in curie:
                        curie = curie.split("|")
                    if isinstance(curie, list):
                        label = [_label(c) for c in curie]
                        if delim:
                            label = delim.join(label)
                    else:
                        label = self.ontology_interface.label(
                            curie, lang=self.settings.preferred_language
                        )
                    for k, _v in copy(obj_as_dict).items():
                        if k == f:
                            obj_as_dict[col_name] = label
        return obj_as_dict

    def emit_dict(self, obj: Mapping[str, Any], object_type: Type = None):
        """
        Write a dictionary object to the stream

        :param obj:
        :param object_type:
        :return:
        """
        raise NotImplementedError

    def emit_header(self, *header: str):
        """
        Emit a header row

        :param header:
        :return:
        """
        for line in header:
            self.line(f"# {line}")
        self.line("#")
