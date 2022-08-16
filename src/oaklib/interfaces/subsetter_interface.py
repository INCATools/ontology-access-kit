from abc import ABC
from dataclasses import dataclass
from typing import Iterator, List

from oaklib.interfaces.basic_ontology_interface import (
    RELATIONSHIP,
    BasicOntologyInterface,
)
from oaklib.types import CURIE, PRED_CURIE


@dataclass
class SubsetStrategy:
    pass


class SyntacticLocalityModuleExtraction(SubsetStrategy):
    module_type: str  # TODO enum


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

    def extract_subset_ontology(
        self, seed_curies: List[CURIE], strategy: SubsetStrategy = None
    ) -> BasicOntologyInterface:
        """
        Extracts an ontology subset using a seed list of curies

        EXPERIMENTAL: this method may be removed in future

        :param seed_curies:
        :param strategy:
        :return:
        """
        raise NotImplementedError

    def gap_fill_relationships(
        self, seed_curies: List[CURIE], predicates: List[PRED_CURIE] = None
    ) -> Iterator[RELATIONSHIP]:
        """
        Given a term subset as a list of curies, find all non-redundant relationships connecting them

        This assumes relation-graph entailed edges, so currently only implemented for ubergraph and sqlite

        First the subset of all entailed edges conforming to the predicate profile connecting any pair of terms in the
        subset is selected

        Then naive transitive reduction on a per predicate basis is performed. This may yield edges that are formally
        redundant, but these are still assumed to be useful for the user

        :param seed_curies:
        :param predicates: if specified, only consider relationships using these predicates
        :return:
        """
        raise NotImplementedError
