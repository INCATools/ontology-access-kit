from abc import ABC
from dataclasses import dataclass
from typing import Dict, List, Tuple

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, RELATIONSHIP
from oaklib.types import CURIE, LABEL, URI, PRED_CURIE


@dataclass
class SubsetStrategy:
    pass


class SyntacticLocalityModuleExtraction(SubsetStrategy):
    module_type: str ## TODO enum


class GraphWalkExtraction(SubsetStrategy):
    predicates: List[PRED_CURIE]


class MireotExtraction(SubsetStrategy):
    pass


class SubsetterInterface(BasicOntologyInterface, ABC):
    """
    an interface that provides subsetting operations

    a challenge here is what a subset operation should produce:

     - an ontology object (committing to a specific object model)
     - an ontology interface
     - a reference to an ontology
    """

    def extract_subset_ontology(self, seed_curies: List[CURIE], strategy: SubsetStrategy = None) -> BasicOntologyInterface:
        """

        :param seed_curies:
        :param strategy:
        :return:
        """
        raise NotImplementedError

    def gap_fill_relationships(self, seed_curies: List[CURIE]) -> List[RELATIONSHIP]:
        """

        :param seed_curies:
        :return:
        """
        raise NotImplementedError



