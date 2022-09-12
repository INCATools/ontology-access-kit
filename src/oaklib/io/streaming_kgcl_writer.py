from dataclasses import dataclass

from kgcl_schema.datamodel.kgcl import Change
from kgcl_schema.grammar.render_operations import render
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.io.streaming_writer import StreamingWriter


@dataclass
class StreamingKGCLWriter(StreamingWriter):
    """
    A writer that streams kgcl changes
    """

    def emit_obj(self, obj: YAMLRoot):
        if isinstance(obj, Change):
            self.file.write(render(obj))
            self.file.write("\n")
        else:
            raise ValueError(f"{obj} is not a change object")
