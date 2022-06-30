from dataclasses import dataclass
from typing import Union

from linkml_runtime.dumpers import json_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.datamodels.obograph import Node
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class StreamingOboJsonWriter(StreamingWriter):
    """
    A writer that emits one OBO Json one node at a time in one stream
    """

    def emit(self, obj: Union[YAMLRoot, CURIE]):
        if isinstance(obj, CURIE):
            self.emit_curie(obj)
        elif isinstance(obj, Node):
            self.emit_curie(obj.id)
        else:
            raise NotImplementedError

    def emit_curie(self, curie: CURIE):
        oi = self.ontology_interface
        if isinstance(oi, OboGraphInterface):
            node = oi.node(curie, include_annotations=True)
            self.line(json_dumper.dumps(node))
