import atexit
import logging
import sys
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Iterable, List, Mapping, Optional, Type, Union

from linkml_runtime import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib import BasicOntologyInterface
from oaklib.datamodels.obograph import Node
from oaklib.types import CURIE
from oaklib.utilities.iterator_utils import chunk

ID_KEY = "id"
LABEL_KEY = "label"


@dataclass
class StreamingWriter(ABC):
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

    def emit(self, obj: Union[YAMLRoot, dict, CURIE], label_fields: Optional[List[str]] = None):
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
            for curie, label in self.ontology_interface.labels(curie_it):
                self.emit(curie, label)

    def emit_curie(self, curie: CURIE, label=None):
        raise NotImplementedError

    def emit_obj(self, obj: YAMLRoot):
        raise NotImplementedError

    def close(self):
        pass

    def finish(self):
        pass

    def line(self, v: str):
        self.file.write(f"{v}\n")

    def add_labels(self, obj_as_dict: Dict, label_fields: Optional[List[str]] = None) -> Dict:
        """
        Adds labels to the object

        :param obj_as_dict:
        :param label_fields:
        :return:
        """
        if label_fields and self.autolabel:
            for f in label_fields:
                curie = obj_as_dict.get(f, None)
                col_name = f"{f}_label"
                if curie and obj_as_dict.get(col_name, None) is None:
                    # allow for a list of CURIEs flattened using a delimiter
                    delim = self.list_delimiter
                    if delim and delim in curie:
                        curie = curie.split("|")
                    if isinstance(curie, list):
                        label = [self.ontology_interface.label(c) for c in curie]
                        if delim:
                            label = delim.join(label)
                    else:
                        label = self.ontology_interface.label(curie)
                    obj_as_dict_new = {}
                    for k, v in obj_as_dict.items():
                        obj_as_dict_new[k] = v
                        if k == f:
                            obj_as_dict_new[col_name] = label
                    obj_as_dict = obj_as_dict_new
        return obj_as_dict

    def emit_dict(self, obj: Mapping[str, Any], object_type: Type = None):
        """
        Write a dictionary object to the stream

        :param obj:
        :param object_type:
        :return:
        """
        raise NotImplementedError
