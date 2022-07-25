from dataclasses import dataclass, field

from funowl import (
    IRI,
    AnnotationAssertion,
    AnnotationProperty,
    AnnotationSubject,
    AnnotationValue,
    Axiom,
    Literal,
    OntologyDocument,
)
from funowl.writers.FunctionalWriter import FunctionalWriter

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
            label = oi.label(curie)
        if label:
            ax = AnnotationAssertion(
                property=AnnotationProperty(oi.curie_to_uri(LABEL_PREDICATE)),
                subject=AnnotationSubject(IRI(oi.curie_to_uri(curie))),
                value=AnnotationValue(Literal(label)),
            )
            self.emit_axiom(ax)

    def emit_axiom(self, axiom: Axiom):
        w = FunctionalWriter()
        self.file.write(str(axiom.to_functional(w)))
        self.file.write("\n")
