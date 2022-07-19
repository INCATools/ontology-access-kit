from abc import ABC
from typing import Any, Iterator, Tuple

from kgcl_schema.datamodel.kgcl import Change, NodeCreation, NodeDeletion

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

TERM_LIST_DIFF = Tuple[CURIE, CURIE]


class DifferInterface(BasicOntologyInterface, ABC):
    """
    Generates descriptions of differences

    TBD: low level diffs vs high level

     See `KGCL <https://github.com/INCATools/kgcl>`_
    """

    def diff(self, other_ontology: BasicOntologyInterface) -> Iterator[Change]:
        """
        Diffs two ontologies

        :param other_ontology:
        :return: TBD KGCL?
        """
        raise NotImplementedError

    def compare_ontology_term_lists(
        self, other_ontology: BasicOntologyInterface
    ) -> Iterator[Change]:
        """
        Provides high level summary of differences

        :param other_ontology:
        :return:
        """
        this_terms = set(self.entities())
        other_terms = set(other_ontology.entities())
        for t in this_terms.difference(other_terms):
            yield NodeDeletion(
                id="x",
                # type='NodeDeletion',
                about_node=t,
            )
        for t in other_terms.difference(this_terms):
            yield NodeCreation(id="x", about_node=t)

    def compare_term_in_two_ontologies(
        self, other_ontology: BasicOntologyInterface, curie: CURIE, other_curie: CURIE = None
    ) -> Any:
        raise NotImplementedError
