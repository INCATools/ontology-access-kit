from abc import ABC
from typing import Dict, List, Tuple

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
import rdflib


class RdfInterface(BasicOntologyInterface, ABC):
    """
    presents ontology as simple RDF graphs, using the rdflib datamodel
    """

    def graph(self) -> rdflib.Graph:
        raise NotImplementedError()

    def triples(self, pattern: Tuple):
        return self.graph().triples(pattern)

    def objects(self, subject, predicate):
        return self.graph().objects(subject, predicate)

