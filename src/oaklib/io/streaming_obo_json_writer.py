from dataclasses import dataclass
from typing import Iterable

from linkml_runtime.dumpers import json_dumper

from oaklib.datamodels.obograph import GraphDocument
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

    def emit_multiple(self, entities: Iterable[CURIE], **kwargs):
        oi = self.ontology_interface
        if isinstance(oi, OboGraphInterface):
            g = oi.extract_graph(list(entities), include_metadata=True)
            gd = GraphDocument(graphs=[g])
            self.line(json_dumper.dumps(gd))
        else:
            raise NotImplementedError
