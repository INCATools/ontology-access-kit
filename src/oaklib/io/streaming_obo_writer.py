import logging
from dataclasses import dataclass
from typing import Any, Iterable

from sssom.constants import OWL_EQUIVALENT_CLASS

from oaklib.converters.obo_graph_to_obo_format_converter import (
    OboGraphToOboFormatConverter,
)
from oaklib.datamodels.obograph import GraphDocument
from oaklib.datamodels.vocabulary import IS_A, RDF_TYPE, SYNONYM_PRED_TO_SCOPE_MAP
from oaklib.interfaces.metadata_interface import MetadataInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class StreamingOboWriter(StreamingWriter):
    """
    A writer that emits one OBO stanza at a time in one stream
    """

    def tag_val(self, k: str, v: Any, xrefs=None):
        self.file.write(f"{k}: {v}")
        if xrefs is not None:
            self.file.write(f' [{", ".join(xrefs)}]')
        self.file.write("\n")

    def emit_curie(self, curie: CURIE, label=None):
        oi = self.ontology_interface
        self.line("[Term]")
        self.line(f"id: {curie}")
        if label is None:
            label = oi.label(curie)
        self.tag_val("name", label)
        defn = oi.definition(curie)
        if defn:
            if isinstance(oi, MetadataInterface):
                _, anns = oi.definition_with_annotations(curie)
            else:
                anns = []
            self.tag_val("def", f'"{defn}"', xrefs=[ann.object for ann in anns])
        for _, x in oi.simple_mappings_by_curie(curie):
            self.line(f"xref: {x}")
        amap = oi.entity_alias_map(curie)
        for a, vs in amap.items():
            if a in SYNONYM_PRED_TO_SCOPE_MAP:
                scope = SYNONYM_PRED_TO_SCOPE_MAP[a]
                for v in vs:
                    self.line(f'synonym: "{v}" {scope} []')
        if isinstance(oi, OboGraphInterface):
            rmap = oi.outgoing_relationship_map(curie)
            for p in rmap.get(IS_A, []):
                self.line(f"is_a: {p} ! {oi.label(p)}")
            for r, ps in rmap.items():
                if r != IS_A and r != RDF_TYPE and r != OWL_EQUIVALENT_CLASS:
                    for p in ps:
                        self.line(f"relationship: {r} {p} ! {oi.label(p)}")
            try:
                for ldef in oi.logical_definitions([curie]):
                    for p in ldef.genusIds:
                        self.line(f"intersection_of: {p} ! {oi.label(p)}")
                    for r in ldef.restrictions:
                        self.line(
                            f"intersection_of: {r.propertyId} {r.fillerId} ! {oi.label(r.fillerId)}"
                        )
            except NotImplementedError:
                logging.info("Logical definitions not implemented")

        self.line("\n")

    def emit_multiple(self, entities: Iterable[CURIE], **kwargs):
        oi = self.ontology_interface
        if isinstance(oi, OboGraphInterface):
            logging.info("Extracting graph")
            g = oi.extract_graph(list(entities), include_metadata=True)
            gd = GraphDocument(graphs=[g])
            logging.info(f"Converting {len(g.nodes)} nodes to OBO")
            converter = OboGraphToOboFormatConverter()
            converter.curie_converter = oi.converter
            obodoc = converter.convert(gd)
            logging.info(f"Writing {len(obodoc.stanzas)} OBO stanzas")
            obodoc.dump(self.file)
        else:
            super().emit_multiple(entities, **kwargs)
