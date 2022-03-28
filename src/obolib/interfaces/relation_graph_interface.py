from abc import ABC
from typing import Dict, List, Tuple

from obolib.interfaces.basic_ontology_interface import BasicOntologyInterface, RELATIONSHIP_MAP
from obolib.types import CURIE, LABEL, URI


class RelationGraphInterface(BasicOntologyInterface, ABC):
    """
    an interface that provides relation graph abstractions
    """

    def entailed_outgoing_relationships_by_curie(self, curie: CURIE) -> RELATIONSHIP_MAP:
        """
        The return relationship map is keyed by relationship type, where the values
        are the 'parents' or fillers

        OWL formulation:

         - is_a: {P : SubClassOf(C P), class(P)}
         - R: {P : SubClassOf(C ObjectSomeValuesFrom( RP), class(P), property(P)}

        :param curie: the 'child' term
        :return:
        """
        raise NotImplementedError()

