import logging
from abc import ABC
from typing import Any, Iterator, Tuple

import kgcl_schema.datamodel.kgcl as kgcl
from kgcl_schema.datamodel.kgcl import Change, NodeCreation, NodeDeletion

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.types import CURIE

TERM_LIST_DIFF = Tuple[CURIE, CURIE]


def _gen_id():
    return "x"


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
        :return: KGCL change object
        """
        for e1 in self.entities():
            logging.debug(f"Comparing e1 {e1}")
            if e1 not in other_ontology.entities():
                yield NodeDeletion(id=_gen_id(), about_node=e1)
                continue
            if not self.different_from(e1, other_ontology):
                continue
            e1_arels = set(self.alias_relationships(e1, exclude_labels=True))
            e2_arels = set(other_ontology.alias_relationships(e1, exclude_labels=True))
            for arel in e1_arels.difference(e2_arels):
                pred, alias = arel
                switches = {r[0] for r in e2_arels if r[1] == alias}
                if len(switches) == 1:
                    e2_arels = set([x for x in e2_arels if x[1] != alias])
                    # TODO: KGCL model needs to include predicates
                    yield kgcl.SynonymPredicateChange(id=_gen_id(), about_node=e1, old_value=alias)
                else:
                    yield kgcl.RemoveSynonym(id=_gen_id(), about_node=e1, old_value=alias)
            for arel in e2_arels.difference(e1_arels):
                pred, alias = arel
                yield kgcl.NewSynonym(id=_gen_id(), about_node=e1, new_value=alias)
            e1_label = self.label(e1)
            e2_label = other_ontology.label(e1)
            if e1_label != e2_label:
                yield kgcl.NodeRename(
                    id=_gen_id(), about_node=e1, old_value=e1_label, new_value=e2_label
                )
            e1_rels = set(self.outgoing_relationships(e1))
            e2_rels = set(other_ontology.outgoing_relationships(e1))
            for rel in e1_rels.difference(e2_arels):
                pred, filler = rel
                edge = kgcl.Edge(subject=e1, predicate=pred, object=filler)
                switches = list({r[0] for r in e2_rels if r[1] == filler})
                if len(switches) == 1:
                    e2_rels = set([x for x in e2_rels if x[1] != filler])
                    yield kgcl.PredicateChange(
                        id=_gen_id(), about_edge=edge, old_value=pred, new_value=switches[0]
                    )
                else:
                    yield kgcl.NodeMove(id=_gen_id(), about_edge=edge, old_value=pred)
            for rel in e2_rels.difference(e1_rels):
                pred, filler = rel
                edge = kgcl.Edge(subject=e1, predicate=pred, object=filler)
                yield kgcl.NodeMove(id=_gen_id(), about_edge=edge, old_value=pred)
        for e2 in other_ontology.entities():
            if e2 not in self.entities():
                yield NodeCreation(id=_gen_id(), about_node=e2)
                continue

    def different_from(self, entity: CURIE, other_ontology: BasicOntologyInterface) -> bool:
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
