from abc import ABC
from typing import Dict, List, Tuple, Iterable, Union

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP, RELATIONSHIP
from oaklib.types import CURIE, LABEL, URI, PRED_CURIE
from oaklib.utilities.graph.relationship_walker import walk_up


class RelationGraphInterface(BasicOntologyInterface, ABC):
    """
    an interface that provides relation graph abstractions

    .. note ::

        that the operations provided here are similar to the graph-walking operations provided in :class:`.OboGraphInterface`.
        The main difference is that a RG provides a more restricted and formally correct set of entailments
    """

    def entailed_outgoing_relationships_by_curie(self, curie: CURIE,
                                                 predicates: List[PRED_CURIE] = None) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        """
        The return relationship map is keyed by relationship type, where the values
        are the 'parents' or fillers

        OWL formulation:

         - is_a: {P : SubClassOf(C P), class(P)}
         - R: {P : SubClassOf(C ObjectSomeValuesFrom( RP), class(P), property(P)}

        :param curie: the 'child' term
        :param predicates:
        :return:
        """
        raise NotImplementedError

    def entailed_incoming_relationships_by_curie(self, curie: CURIE,
                                                 predicates: List[PRED_CURIE] = None) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        """
        The return relationship map is keyed by relationship type, where the values
        are the 'parents' or fillers

        OWL formulation:

         - is_a: {P : SubClassOf(C P), class(P)}
         - R: {P : SubClassOf(C ObjectSomeValuesFrom( RP), class(P), property(P)}

        :param curie: the 'child' term
        :param predicates:
        :return:
        """
        raise NotImplementedError

    def walk_up_relationship_graph(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[RELATIONSHIP]:
        """
        Walks up the relation graph from a seed set of curies or individual curie, returning the full ancestry graph

        Note: this may be inefficient for remote endpoints, in future a graph walking endpoint will implement this

        :param start_curies:
        :param predicates:
        :return:
        """
        return walk_up(self, start_curies, predicates=predicates)

    def xxxancestors(self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None) -> Iterable[CURIE]:
        # TODO: make reflexivity a parameters
        ancs = set([x[2] for x in self.walk_up_relationship_graph(start_curies, predicates)] + [start_curies])
        for a in ancs:
            yield a


