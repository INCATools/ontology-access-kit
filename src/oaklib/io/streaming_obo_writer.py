from dataclasses import dataclass
from typing import Union, Any

from linkml_runtime.utils.yamlutils import YAMLRoot
from oaklib import BasicOntologyInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class StreamingOboWriter(StreamingWriter):
    """
    A writer that emits one document at a time in one stream
    """

    def emit(self, obj: Union[YAMLRoot, str]):
        if isinstance(obj, str):
            self.emit_curie(obj)
        else:
            raise NotImplementedError

    def tag_val(self, k: str, v: Any, xrefs=None):
        self.file.write(f'{k}: {v}')
        if xrefs is not None:
            self.file.write(f' [{", ".join(xrefs)}]')
        self.file.write('\n')

    def emit_curie(self, curie: CURIE):
        file = self.file
        oi = self.ontology_interface
        self.line(f'[Term]')
        self.line(f'id: {curie}')
        self.tag_val('name', oi.get_label_by_curie(curie))
        defn = oi.get_definition_by_curie(curie)
        if defn:
            self.tag_val('def', f'"{defn}"', xrefs=[])
        for prop, x in oi.get_simple_mappings_by_curie(curie):
            self.line(f'xref: {x}')
        self.line('\n')

