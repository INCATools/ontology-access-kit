from abc import ABC
from typing import Dict, List, Tuple, Any, Iterator

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
import rdflib
from oaklib.types import CURIE, PRED_CURIE
from rdflib import URIRef

TRIPLE = Tuple[CURIE, PRED_CURIE, Any]
RDF_TRIPLE = Tuple[URIRef, URIRef, Any]

class RdfInterface(BasicOntologyInterface, ABC):
    """
    presents ontology as simple RDF graphs, using the rdflib datamodel
    """

    def graph(self) -> rdflib.Graph:
        raise NotImplementedError()

    def _triple_as_urirefs(self, triple: TRIPLE) -> RDF_TRIPLE:
        pass

    def _triple_as_curies(self, triple: RDF_TRIPLE) -> TRIPLE:
        pass

    def triples(self, pattern: TRIPLE) -> Iterator[TRIPLE]:
        for t in self.graph().triples(self._triple_as_urirefs(pattern)):
            yield self._triple_as_curies(t)

    def objects(self, subject, predicate) -> Iterator[Any]:
        return self.graph().objects(subject, predicate)

    def extract_triples(self, seed_curies: List[CURIE], predicates: List[PRED_CURIE] = None, strategy: str = None,
                        map_to_curies=True) -> Iterator[TRIPLE]:
        pass

