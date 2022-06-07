from dataclasses import dataclass
from typing import Union, Any

from linkml_runtime.utils.yamlutils import YAMLRoot
from oaklib import BasicOntologyInterface
from oaklib.datamodels.vocabulary import IS_A, SYNONYM_PRED_TO_SCOPE_MAP
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
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
        if isinstance(oi, MetadataInterface):
            axioms = list(oi.statements_with_annotations(curie))
        else:
            axioms = []
        self.line(f'[Term]')
        self.line(f'id: {curie}')
        self.tag_val('name', oi.get_label_by_curie(curie))
        defn = oi.get_definition_by_curie(curie)
        if defn:
            if isinstance(oi, MetadataInterface):
                _, anns = oi.definition_with_annotations(curie)
            else:
                anns = []
            self.tag_val('def', f'"{defn}"', xrefs=[ann.object for ann in anns])
        for prop, x in oi.get_simple_mappings_by_curie(curie):
            self.line(f'xref: {x}')
        amap = oi.alias_map_by_curie(curie)
        for a, vs in amap.items():
            if a in SYNONYM_PRED_TO_SCOPE_MAP:
                scope = SYNONYM_PRED_TO_SCOPE_MAP[a]
                for v in vs:
                    self.line(f'synonym: "{v}" {scope} []')
        if isinstance(oi, OboGraphInterface):
            rmap = oi.get_outgoing_relationships_by_curie(curie)
            for p in rmap.get(IS_A, []):
                self.line(f'is_a: {p} ! {oi.get_label_by_curie(p)}')
            for r, ps in rmap.items():
                if r != IS_A:
                    for p in ps:
                        self.line(f'relationship: {r} {p} ! {oi.get_label_by_curie(p)}')
        self.line('\n')

