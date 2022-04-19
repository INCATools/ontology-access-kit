import sys
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StreamingWriter:
    """
    Base class for streaming writers
    """
    file: Any = field(default_factory=lambda: sys.stdout)

    def close(self):
        pass