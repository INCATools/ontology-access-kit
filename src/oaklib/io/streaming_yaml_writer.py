import csv
import sys
from dataclasses import dataclass, field
from typing import Any

from linkml_runtime import CurieNamespace
from linkml_runtime.dumpers import yaml_dumper
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
class StreamingYamlWriter(StreamingWriter):
    """
    A writer that emits one document at a time in one stream
    """

    def emit(self, obj: YAMLRoot):
        self.file.write(yaml_dumper.dumps(obj))
        self.file.write("\n---\n")


