from abc import ABC
from typing import Dict, List, Tuple

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.types import CURIE, LABEL, URI
from rdflib import Graph


class RdfInterface(BasicOntologyInterface, ABC):
    """
    presents ontology as simple RDF graphs
    """

    def graph(self) -> Graph:
        raise NotImplementedError()

    def triples(self, pattern: Tuple):
        return self.graph().triples(pattern)

    def objects(self, subject, predicate):
        return self.graph().objects(subject, predicate)

