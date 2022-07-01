from dataclasses import dataclass, field

import rdflib
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot

from oaklib.datamodels.vocabulary import IS_A, SYNONYM_PRED_TO_SCOPE_MAP, LABEL_PREDICATE
from oaklib.io.streaming_writer import StreamingWriter, ID_KEY, LABEL_KEY
from oaklib.types import CURIE
from rdflib import Literal
from rdflib.term import Node


@dataclass
class StreamingRdfWriter(StreamingWriter):
    """
    A writer that emits one frame at a time in RDF
    """
    graph: rdflib.Graph = None
    dialect: str = field(default_factory=lambda: 'ttl')

    def emit_curie(self, curie: CURIE, label=None):
        oi = self.ontology_interface
        if label is None:
            label = oi.get_label_by_curie(curie)
        if label:
            self.add_triple(oi.curie_to_uri(curie), oi.curie_to_uri(LABEL_PREDICATE), rdflib.Literal(label))

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
        self.file.write(self.graph.serialize(format=self.dialect))

