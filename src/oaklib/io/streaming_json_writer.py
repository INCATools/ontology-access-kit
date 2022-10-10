import json
from dataclasses import dataclass, field
from typing import Any, Type, Union

from linkml_runtime import CurieNamespace
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


def _keyval(x: Any) -> str:
    if isinstance(x, CurieNamespace):
        return str(x.curie())
    # if isinstance(x, EnumDefinitionImpl):
    #    if x.curie:
    #        return str(x.curie)
    return str(x)


@dataclass
class StreamingJsonWriter(StreamingWriter):
    """
    A writer that emits one document at a time in one stream

    """

    current_entry_number: int = field(default_factory=lambda: 0)

    def emit(self, obj: Union[YAMLRoot, dict, str], label_fields=None):
        if self.current_entry_number == 0:
            self.file.write("[\n")
        else:
            self.file.write(",\n")
        self.current_entry_number += 1
        if isinstance(obj, dict):
            self.file.write(json.dumps(obj, indent=4, sort_keys=True))
        elif isinstance(obj, YAMLRoot):
            self.file.write(json_dumper.dumps(obj))
        else:
            oi = self.ontology_interface
            if isinstance(oi, OboGraphInterface):
                node = oi.node(obj, include_metadata=True)
                self.line(json_dumper.dumps(node))
            # self.file.write(json_dumper.dumps(obj))
        self.file.write("\n")

    def emit_curie(self, curie: CURIE, label=None):
        raise NotImplementedError

    def finish(self):
        self.file.write("]\n")

    def emit_dict(self, obj: dict, object_type: Type = None):
        self.file.write(json.dumps(obj, indent=4, sort_keys=True))
