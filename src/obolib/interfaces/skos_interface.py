from abc import ABC
from typing import Dict, List, Tuple, Iterable

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.types import CURIE, LABEL, URI
from rdflib import Graph


class SkosInterface(BasicOntologyInterface, ABC):
    """
    presents ontology as simple SKOS vocabularies
    """

    def concepts(self) -> Iterable[CURIE]
        raise NotImplementedError

    def broader(self, curie: CURIE) -> Iterable[CURIE]
        raise NotImplementedError

    def narrower(self, curie: CURIE) -> Iterable[CURIE]
        raise NotImplementedError

    def exact(self, curie: CURIE) -> Iterable[CURIE]
        raise NotImplementedError

    def related(self, curie: CURIE) -> Iterable[CURIE]
        raise NotImplementedError


