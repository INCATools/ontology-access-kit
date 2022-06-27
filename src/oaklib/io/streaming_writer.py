import sys
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, List, Union

from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib import BasicOntologyInterface
from oaklib.types import CURIE


@dataclass
class StreamingWriter(ABC):
    """
    Base class for streaming writers
    """

    file: Any = field(default_factory=lambda: sys.stdout)
    ontology_interface: BasicOntologyInterface = None
    display_options: List[str] = None
    autolabel: bool = None

    def emit(self, obj: Union[YAMLRoot, dict, CURIE], label_fields=None):
        raise NotImplementedError

    def close(self):
        pass

    def line(self, v: str):
        self.file.write(f"{v}\n")
