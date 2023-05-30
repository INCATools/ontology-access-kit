from abc import ABC
from typing import Iterable, List, Tuple

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE, PRED_CURIE


class RelationGraphInterface(BasicOntologyInterface, ABC):
    """
    An interface that provides relation graph abstractions.

    .. note ::

        this interface is now largely subsumed into the BasicOntologyInterface
    """

    def entailed_outgoing_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
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

    def entailed_outgoing_relationships_by_curie(
        self, *args, **kwargs
    ) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        return self.entailed_outgoing_relationships(*args, **kwargs)

    def entailed_incoming_relationships(
        self, curie: CURIE, predicates: List[PRED_CURIE] = None
    ) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
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

    def entailed_incoming_relationships_by_curie(
        self, *args, **kwargs
    ) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        return self.entailed_incoming_relationships(*args, **kwargs)

    def entailed_relationships_between(self, subject: CURIE, object: CURIE) -> Iterable[PRED_CURIE]:
        """
        Yield the predicates of all valid relationships connecting subject and object, both direct and indirect

        :param subject:
        :param object:
        :return:
        """
        raise NotImplementedError
