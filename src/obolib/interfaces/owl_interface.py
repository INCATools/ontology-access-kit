from abc import ABC
from typing import Dict, List, Tuple

# TODO: add funowl to dependencies
from funowl import Ontology, Axiom
from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface
from obolib.types import CURIE, LABEL, URI
from rdflib import Graph


class OwlInterface(BasicOntologyInterface, ABC):
    """
    presents ontology as an OWL ontology using an OWL datamodel

    We leverage the funowl
    """

    def owl_ontology(self) -> Ontology:
        raise NotImplementedError()

    def axioms(self) -> List[Axiom]:
        return self.owl_ontology().axioms

