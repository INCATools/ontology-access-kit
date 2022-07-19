import logging
from dataclasses import dataclass, field

import rdflib
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib.term import Node

from oaklib.datamodels.vocabulary import LABEL_PREDICATE
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class StreamingRdfWriter(StreamingWriter):
    """
    A writer that emits one frame at a time in RDF
    """

    graph: rdflib.Graph = None
    dialect: str = field(default_factory=lambda: "ttl")

    def emit_curie(self, curie: CURIE, label=None):
        oi = self.ontology_interface
        if label is None:
            label = oi.label(curie)
        if label:
            self.add_triple(
                oi.curie_to_uri(curie), oi.curie_to_uri(LABEL_PREDICATE), rdflib.Literal(label)
            )

    def emit_obj(self, obj: YAMLRoot):
        if self.graph is None:
            self.graph = rdflib.Graph()
        g = rdflib_dumper.as_rdf_graph(obj, schemaview=self.schemaview)
        for t in g:
            self.graph.add(t)

    def add_triple(self, s: str, p: str, o: Node):
        if self.graph is None:
            self.graph = rdflib.Graph()
        self.graph.add((rdflib.URIRef(s), rdflib.URIRef(p), o))

    def close(self):
        if self.graph is None:
            logging.warning("No triples found in graph")
        else:
            self.file.write(self.graph.serialize(format=self.dialect))
