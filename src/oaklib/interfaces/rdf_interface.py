from abc import ABC
from typing import Any, Iterator, List, Tuple

import rdflib
from rdflib import URIRef

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, PRED_CURIE

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
        """
        All triples matching triple pattern

        :param pattern: tuple of s,p,o, where None matches anything
        :return:
        """
        for t in self.graph().triples(self._triple_as_urirefs(pattern)):
            yield self._triple_as_curies(t)

    def objects(self, subject, predicate) -> Iterator[Any]:
        """
        queries objects based on s,p

        :param subject:
        :param predicate:
        :return:
        """
        for obj in self.graph().objects(subject, predicate):
            if isinstance(obj, URIRef):
                yield self.uri_to_curie(obj)
            else:
                yield obj

    def extract_triples(
        self,
        seed_curies: List[CURIE],
        predicates: List[PRED_CURIE] = None,
        strategy: str = None,
        map_to_curies=True,
    ) -> Iterator[TRIPLE]:
        """
        Finds all triples reachable from a seed set

        :param seed_curies:
        :param predicates:
        :param strategy:
        :param map_to_curies:
        :return:
        """
