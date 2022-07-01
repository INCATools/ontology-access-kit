from dataclasses import dataclass, field

import rdflib
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib.term import Node

from funowl import OntologyDocument, Axiom, AnnotationAssertion, Literal, IRI, AnnotationProperty, AnnotationSubject, \
    AnnotationValue

from oaklib.datamodels.vocabulary import LABEL_PREDICATE
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class StreamingOwlFunctionalWriter(StreamingWriter):
    """
    A writer that emits one axiom at a time in OWL
    """

    ontology_document: OntologyDocument = None
    dialect: str = field(default_factory=lambda: "ttl")

    def emit_curie(self, curie: CURIE, label=None):
        oi = self.ontology_interface
        if label is None:
            label = oi.get_label_by_curie(curie)
        if label:
            ax = AnnotationAssertion(
                property=AnnotationProperty(oi.curie_to_uri(LABEL_PREDICATE)),
                subject=AnnotationSubject(IRI(oi.curie_to_uri(curie))),
                value=AnnotationValue(Literal(label))
            )
            self.emit_axiom(ax)


    def emit_axiom(self, axiom: Axiom):
        self.file.write(axiom)

    def close(self):
        self.file.write(self.graph.serialize(format=self.dialect))
