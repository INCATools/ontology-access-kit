import csv
import sys
from dataclasses import dataclass, field
from typing import Any

from linkml_runtime import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.yamlutils import YAMLRoot

def _keyval(x: Any) -> str:
    if isinstance(x, CurieNamespace):
        return str(x.curie())
    #if isinstance(x, EnumDefinitionImpl):
    #    if x.curie:
    #        return str(x.curie)
    return str(x)


@dataclass
class StreamingCsvWriter:
    file: Any = field(default_factory=lambda: sys.stdout)
    header_emitted: bool = None
    delimiter: str = '\t'
    writer: csv.DictWriter = None

    def emit(self, obj: YAMLRoot):
        if self.writer is None:
            self.writer = csv.DictWriter(self.file, delimiter=self.delimiter, fieldnames=list(vars(obj)))
            self.writer.writeheader()
        self.writer.writerow({k: _keyval(v) for k, v in vars(obj).items()})


