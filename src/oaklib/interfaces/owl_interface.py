from abc import ABC
from enum import Enum
from typing import Dict, List, Tuple, Iterable, Optional

# TODO: add funowl to dependencies
from funowl import Ontology, Axiom, Class, SubClassOf, EquivalentClasses
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, LABEL, URI
from rdflib import Graph


class OwlProfile(Enum):
    EL = "EL"
    DL = "DL"
    OWL_FULL = "OWL-Full"
    RL = "RL"
    QC = "QL"

@dataclass
class ReasonerConfiguration:
    reasoner: str = None
    reasoner_version: str = None
    implements_profiles: List[OwlProfile] = None

class OwlInterface(BasicOntologyInterface, ABC):
    """
    presents ontology as an OWL ontology using an OWL datamodel

    We leverage the funowl datamodel

    In future there will be a variety of implementations:

    - funowl
    - owlery
    - owllink servers
    - robot/owlapi via py4j
    """

    def owl_ontology(self) -> Ontology:
        raise NotImplementedError

    def axioms(self, reasoner: Optional[ReasonerConfiguration] = None) -> Iterable[Axiom]:
        raise NotImplementedError

    def subclass_axioms(self, subclass: CURIE = None, superclass: CURIE = None, reasoner: Optional[ReasonerConfiguration] = None) -> Iterable[SubClassOf]:
        """
        Gets all SubClassOf axioms matching criterion

        :param subclass: if specified, constrains to axioms where this is the subclass
        :param superclass: if specified, constrains to axioms where this is the superclass
        :param reasoner:
        :return:
        """
        raise NotImplementedError

    def equivalence_axioms(self, about: CURIE = None, references: CURIE = None, reasoner: Optional[ReasonerConfiguration] = None):
        raise NotImplementedError

    def owl_classes(self) -> Iterable[Class]:
        raise NotImplementedError

    def owl_individuals(self) -> Iterable[Class]:
        raise NotImplementedError

    def is_satisfiable(self, curie: CURIE) -> bool:
        raise NotImplementedError

    def reasoner_configurations(self) -> List[ReasonerConfiguration]:
        raise NotImplementedError

