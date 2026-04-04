from dataclasses import dataclass, field
from typing import Any

import pyhornedowl
from pyhornedowl.model import IRI, Annotation, AnnotationAssertion, AnnotationProperty, SimpleLiteral

from oaklib.datamodels.vocabulary import LABEL_PREDICATE
from oaklib.io.streaming_writer import StreamingWriter
from oaklib.types import CURIE


@dataclass
class StreamingOwlFunctionalWriter(StreamingWriter):
    """
    A writer that emits one axiom at a time in OWL
    """

    ontology_document: pyhornedowl.PyIndexedOntology = None
    dialect: str = field(default_factory=lambda: "ttl")

    def emit_curie(self, curie: CURIE, label=None):
        oi = self.ontology_interface
        if label is None:
            label = oi.label(curie)
        if label:
            axiom = AnnotationAssertion(
                IRI.parse(oi.curie_to_uri(curie)),
                Annotation(
                    AnnotationProperty(IRI.parse(oi.curie_to_uri(LABEL_PREDICATE))),
                    SimpleLiteral(label),
                ),
            )
            self.emit_axiom(axiom)

    def emit_axiom(self, axiom: Any):
        self.file.write(str(axiom))
        self.file.write("\n")
