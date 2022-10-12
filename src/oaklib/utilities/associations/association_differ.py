import logging
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from typing import Iterator, List, Mapping, Set, Tuple

from oaklib.datamodels.association import Association
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.subsets.slimmer_utils import filter_redundant

CHANGE = Tuple[CURIE, str, CURIE]


@dataclass
class AssociationDiff:
    changes: List[CHANGE] = None
    set1_terms: List[CURIE] = None
    set2_terms: List[CURIE] = None


@dataclass
class AssociationDiffer:
    """Engine for performing diffs between associations."""

    ontology_interface: OboGraphInterface

    def changes(
        self,
        assocs1: List[Association],
        assocs2: List[Association],
        predicates: List[PRED_CURIE],
    ) -> Iterator[CHANGE]:
        """
        Perform diff on two association collections.

        :param assocs1:
        :param assocs2:
        :param predicates:
        :return:
        """
        logging.info("Creating map for first set")
        am1 = self.create_entity_to_term_map(assocs1, predicates)
        logging.info("Creating map for second set")
        am2 = self.create_entity_to_term_map(assocs2, predicates)
        entities = set(am1.keys()).union(set(am2.keys()))
        logging.info(f"Comparing {len(entities)}")
        for entity in entities:
            for change in self._compare_set_pair(
                entity, am1.get(entity, set()), am2.get(entity, set()), predicates
            ):
                yield change

    def compare(
        self,
        assocs1: List[Association],
        assocs2: List[Association],
        predicates: List[PRED_CURIE],
    ) -> AssociationDiff:
        diffs = list(self.changes(assocs1, assocs2, predicates))
        diff = AssociationDiff(diffs)
        return diff

    def create_entity_to_term_map(
        self, assocs: List[Association], predicates: List[PRED_CURIE] = None
    ) -> Mapping[CURIE, Set[CURIE]]:
        m = defaultdict(set)
        for assoc in assocs:
            m[assoc.subject].add(assoc.object)
        for k, vs in copy(m).items():
            # use ancestor closure
            m[k] = set(
                self.ontology_interface.ancestors(list(vs), predicates=predicates, reflexive=True)
            )
        return m

    def _compare_set_pair(
        self, entity: CURIE, set1: Set[CURIE], set2: Set[CURIE], predicates: List[PRED_CURIE] = None
    ) -> Iterator[CHANGE]:
        oi = self.ontology_interface
        for x in filter_redundant(oi, set1.difference(set2), predicates=predicates):
            yield entity, "set1", x
        for x in filter_redundant(oi, set2.difference(set1), predicates=predicates):
            yield entity, "set2", x
