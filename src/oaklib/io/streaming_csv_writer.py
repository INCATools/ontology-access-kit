import csv
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, Union

from linkml_runtime import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.yamlutils import YAMLRoot
from oaklib.io.streaming_writer import StreamingWriter


def _keyval(x: Any) -> str:
    if isinstance(x, CurieNamespace):
        return str(x.curie())
    #if isinstance(x, EnumDefinitionImpl):
    #    if x.curie:
    #        return str(x.curie)
    return str(x)


@dataclass
class StreamingCsvWriter(StreamingWriter):
    """
    A writer that streams CSV/TSV output
    """

    header_emitted: bool = None
    delimiter: str = '\t'
    writer: csv.DictWriter = None

    def emit(self, obj: Union[YAMLRoot, Dict]):
        if isinstance(obj, dict):
            obj_as_dict = obj
        else:
            obj_as_dict = vars(obj)
        if self.writer is None:
            self.writer = csv.DictWriter(self.file, delimiter=self.delimiter, fieldnames=list(obj_as_dict))
            self.writer.writeheader()
        self.writer.writerow({k: _keyval(v) for k, v in obj_as_dict.items()})


