import sys
from dataclasses import dataclass, field
from typing import Any, List

from oaklib import BasicOntologyInterface


@dataclass
class StreamingWriter:
    """
    Base class for streaming writers
    """
    file: Any = field(default_factory=lambda: sys.stdout)
    ontology_interface: BasicOntologyInterface = None
    display_options: List[str] = None

    def close(self):
        pass

    def line(self, v: str):
        self.file.write(f'{v}\n')