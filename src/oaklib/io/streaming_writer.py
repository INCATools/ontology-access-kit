import atexit
import sys
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, List, Union

from linkml_runtime import SchemaView
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib import BasicOntologyInterface
from oaklib.datamodels.obograph import Node
from oaklib.types import CURIE

ID_KEY = "id"
LABEL_KEY = "label"


@dataclass
class StreamingWriter(ABC):
    """
    Base class for streaming writers
    """

    file: Any = field(default_factory=lambda: sys.stdout)
    ontology_interface: BasicOntologyInterface = None
    display_options: List[str] = None
    autolabel: bool = None
    schemaview: SchemaView = None
    _output: Any = None

    def __post_init__(self):
        atexit.register(self.close)

    @property
    def output(self) -> str:
        return self._output

    @output.setter
    def output(self, value) -> None:
        self._output = value
        if self._output is not None:
            if isinstance(self._output, str):
                self.file = open(self._output, "w", encoding="UTF-8")
            else:
                self.file = self._output

    def emit(self, obj: Union[YAMLRoot, dict, CURIE], label_fields=None):
        if isinstance(obj, CURIE):
            self.emit_curie(obj)
        elif isinstance(obj, Node):
            self.emit_curie(obj.id)
        elif isinstance(obj, dict):
            self.emit_curie(obj[ID_KEY], obj.get(LABEL_KEY, None))
        else:
            self.emit_obj(obj)

    def emit_curie(self, curie: CURIE, label=None):
        raise NotImplementedError

    def emit_obj(self, obj: YAMLRoot):
        raise NotImplementedError

    def close(self):
        pass

    def line(self, v: str):
        self.file.write(f"{v}\n")
