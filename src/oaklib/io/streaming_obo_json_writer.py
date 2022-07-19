from dataclasses import dataclass

from linkml_runtime.dumpers import json_dumper

from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class StreamingOboJsonWriter(StreamingWriter):
    """
    A writer that emits one OBO Json one node at a time in one stream
    """

    def emit_curie(self, curie: CURIE, label=None):
        oi = self.ontology_interface
        if isinstance(oi, OboGraphInterface):
            node = oi.node(curie, include_metadata=True)
            self.line(json_dumper.dumps(node))
        else:
            raise NotImplementedError
