import logging
from abc import ABC
from dataclasses import dataclass
from typing import Iterator, List

from oaklib.datamodels.obograph import Graph
from oaklib.interfaces import OboGraphInterface
from oaklib.interfaces.basic_ontology_interface import (
    RELATIONSHIP,
    BasicOntologyInterface,
)
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.obograph_utils import index_graph_nodes


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
    an interface that provides subsetting operations.

    Subsets are named sets of entities/terms in an ontology. Subsetting operations include
    extracting, and "rolling up" to a subset.

    See:

     - http://geneontology.org/docs/go-subset-guide/

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
        Given a term subset as a list of curies, find all non-redundant relationships connecting them.

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

    def extract_gap_filled_graph(
        self,
        seed_curies: List[CURIE],
        predicates: List[PRED_CURIE] = None,
        include_singletons: bool = True,
        **kwargs,
    ) -> Graph:
        rels = list(self.gap_fill_relationships(seed_curies, predicates=predicates))
        logging.info(f"Gap filled relationships: {len(rels)}")
        if not isinstance(self, OboGraphInterface):
            raise AssertionError(f"{self} needs to of type OboGraphInterface")
        graph = self.relationships_to_graph(rels)
        ix = index_graph_nodes(graph)
        logging.info(f"Gap filled nodes: {len(ix)}")
        if include_singletons:
            for c in seed_curies:
                if c not in ix:
                    node = self.node(c)
                    logging.info(f"Adding: {node}")
                    graph.nodes.append(node)
                    # graph.edges.append(Edge(sub=c, pred="subClassOf", obj=c))
        return graph
