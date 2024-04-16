import logging
from dataclasses import dataclass
from typing import Any, Iterable

from oaklib.converters.obo_graph_to_obo_format_converter import (
    OboGraphToOboFormatConverter,
)
from oaklib.datamodels.obograph import (
    DisjointClassExpressionsAxiom,
    Graph,
    GraphDocument,
    LogicalDefinitionAxiom,
)
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class StreamingOboWriter(StreamingWriter):
    """
    A writer that emits one OBO stanza at a time in one stream
    """

    converter: OboGraphToOboFormatConverter = None

    def tag_val(self, k: str, v: Any, xrefs=None):
        self.file.write(f"{k}: {v}")
        if xrefs is not None:
            self.file.write(f' [{", ".join(xrefs)}]')
        self.file.write("\n")

    def emit_curie(self, curie: CURIE, label=None):
        oi = self.ontology_interface
        if self.converter is None:
            self.converter = OboGraphToOboFormatConverter()
        if not isinstance(oi, OboGraphInterface):
            raise NotImplementedError
        graph = oi.direct_graph(curie)
        ext_graph = Graph(id="ext", nodes=[n for n in graph.nodes if n.id != curie])
        graph.nodes = [n for n in graph.nodes if n.id == curie]
        text = self.converter.dumps(graph, aux_graphs=[ext_graph])
        self.file.write(text)

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

    def emit_obj(self, obj: Any, **kwargs):
        oi = self.ontology_interface
        if isinstance(obj, CURIE):
            self.emit_curie(obj)
        elif isinstance(obj, LogicalDefinitionAxiom):
            self.line("[Term]")
            self.line(f"id: {obj.definedClassId} ! {oi.label(obj.definedClassId)}")
            for genus in obj.genusIds:
                self.line(f"intersection_of: {genus} ! {oi.label(genus)}")
            for r in obj.restrictions:
                self.line(f"intersection_of: {r.propertyId} {r.fillerId} ! {oi.label(r.fillerId)}")
            self.line("\n")
        elif isinstance(obj, DisjointClassExpressionsAxiom):
            if len(obj.classIds) > 1:
                for i1, c1 in enumerate(obj.classIds):
                    for i2, c2 in enumerate(obj.classIds):
                        if i1 >= i2:
                            continue
                        self.line("[Term]")
                        self.line(f"id: {c1} ! {oi.label(c1)}")
                        self.line(f"disjoint_from: {c2} ! {oi.label(c2)}")
                        self.line("\n")
            else:
                logging.warning(
                    f"Skipping DisjointClassExpressionsAxiom with only one class: {obj}"
                )
        else:
            raise NotImplementedError(f"Cannot emit type {type(obj)} {obj}")
