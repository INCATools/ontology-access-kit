import logging
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from typing import Iterator, List, Mapping, Set, Tuple

from oaklib.datamodels.association import Association, AssociationChange
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE
from oaklib.utilities.basic_utils import pairs_as_dict
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

    adapter: OboGraphInterface

    _obsoletion_map: Mapping[CURIE, List[CURIE]] = None

    set1_name: str = field(default_factory=lambda: "set1")
    set2_name: str = field(default_factory=lambda: "set2")

    def calculate_change_tuples(
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

    def calculate_change_objects(
        self,
        assocs1: List[Association],
        assocs2: List[Association],
        predicates: List[PRED_CURIE],
    ) -> Iterator[AssociationChange]:
        obsoletion_map = self.obsoletion_map
        subject_map1 = pairs_as_dict([(a.subject, a) for a in assocs1])
        subject_map2 = pairs_as_dict([(a.subject, a) for a in assocs2])
        entities = set(subject_map1.keys()).union(set(subject_map2.keys()))
        for entity in entities:
            if entity not in subject_map1:
                for a in subject_map2[entity]:
                    yield AssociationChange(
                        subject=a.subject,
                        new_object=a.object,
                        is_creation=True,
                    )
                continue
            if entity not in subject_map2:
                for a in subject_map1[entity]:
                    yield AssociationChange(
                        subject=a.subject,
                        old_object=a.object,
                        is_deletion=True,
                    )
                continue
            objects1 = set([a.object for a in subject_map1[entity]])
            objects2 = set([a.object for a in subject_map2[entity]])
            accounted_for_in_objects2 = set()
            for o in objects1.difference(objects2):
                old_object_obsolete = False
                if o in obsoletion_map:
                    old_object_obsolete = True
                    ixn = objects2.intersection(obsoletion_map[o])
                    if ixn:
                        for o2 in ixn:
                            yield AssociationChange(
                                subject=entity,
                                old_object=o,
                                new_object=o2,
                                is_migration=True,
                                old_object_obsolete=old_object_obsolete,
                            )
                    continue
                if not predicates:
                    yield AssociationChange(
                        subject=entity,
                        old_object=o,
                        is_deletion=True,
                        old_object_obsolete=old_object_obsolete,
                        closure_predicates=[],
                    )
                    continue
                o_ancestors = list(
                    self.adapter.ancestors([o], predicates=predicates, reflexive=True)
                )
                ixn = objects2.intersection(o_ancestors)
                if ixn:
                    o2 = ixn.pop()
                    accounted_for_in_objects2.add(o2)
                    yield AssociationChange(
                        subject=entity,
                        old_object=o,
                        new_object=o2,
                        is_generalization=True,
                        old_object_obsolete=old_object_obsolete,
                        closure_predicates=predicates,
                    )
                    continue
                o2_ancestors = list(
                    self.adapter.ancestors(list(objects2), predicates=predicates, reflexive=True)
                )
                # o_descendants = list(
                #    self.adapter.descendants([o], predicates=predicates, reflexive=True)
                # )
                # ixn = objects2.intersection(o_descendants)
                if o in o2_ancestors:
                    new_object = None
                    for o2 in objects2:
                        if o in list(
                            self.adapter.ancestors([o2], predicates=predicates, reflexive=True)
                        ):
                            new_object = o2
                            break
                    # o2 = ixn.pop()
                    accounted_for_in_objects2.add(new_object)
                    yield AssociationChange(
                        subject=entity,
                        old_object=o,
                        new_object=new_object,
                        is_specialization=True,
                        old_object_obsolete=old_object_obsolete,
                        closure_predicates=predicates,
                    )
                    continue
                # neither specialization nor generalization
                yield AssociationChange(
                    subject=entity,
                    old_object=o,
                    is_deletion=True,
                    old_object_obsolete=old_object_obsolete,
                    closure_predicates=predicates,
                )
            for o in objects2.difference(objects1):
                if o in accounted_for_in_objects2:
                    continue
                yield AssociationChange(
                    subject=entity,
                    new_object=o,
                    is_creation=True,
                    closure_predicates=predicates,
                )

    def compare(
        self,
        assocs1: List[Association],
        assocs2: List[Association],
        predicates: List[PRED_CURIE],
    ) -> AssociationDiff:
        diffs = list(self.calculate_change_tuples(assocs1, assocs2, predicates))
        diff = AssociationDiff(diffs)
        return diff

    def create_entity_to_term_map(
        self, assocs: List[Association], predicates: List[PRED_CURIE] = None
    ) -> Mapping[CURIE, Set[CURIE]]:
        """
        Create a map from entity to term closures.

        :param assocs:
        :param predicates:
        :return:
        """
        m = defaultdict(set)
        for assoc in assocs:
            m[assoc.subject].add(assoc.object)
        for k, vs in copy(m).items():
            # use ancestor closure
            m[k] = set(self.adapter.ancestors(list(vs), predicates=predicates, reflexive=True))
        return m

    def _compare_set_pair(
        self, entity: CURIE, set1: Set[CURIE], set2: Set[CURIE], predicates: List[PRED_CURIE] = None
    ) -> Iterator[CHANGE]:
        oi = self.adapter
        for x in filter_redundant(oi, set1.difference(set2), predicates=predicates):
            yield entity, self.set1_name, x
        for x in filter_redundant(oi, set2.difference(set1), predicates=predicates):
            yield entity, self.set2_name, x

    def changes_by_publication(
        self,
        assocs1: List[Association],
        assocs2: List[Association],
        predicates: List[PRED_CURIE],
    ) -> Iterator[AssociationChange]:
        """
        Perform diff on two association collections.

        :param assocs1:
        :param assocs2:
        :param predicates:
        :return:
        """

        def _canonical_pub_id(pubs: List[CURIE]) -> CURIE:
            pmids = [p for p in pubs if p.startswith("PMID:")]
            if pmids:
                return pmids[0]
            return pubs[0]

        pubmap1 = pairs_as_dict(
            [(_canonical_pub_id(a.publications), a) for a in assocs1 if a.publications]
        )
        pubmap2 = pairs_as_dict(
            [(_canonical_pub_id(a.publications), a) for a in assocs2 if a.publications]
        )
        pubs_in_common = set(pubmap1.keys()).intersection(set(pubmap2.keys()))
        for pub in pubs_in_common:
            for change in self.calculate_change_objects(pubmap1[pub], pubmap2[pub], predicates):
                change.publications = [pub]
                change.summary_group = pub
                yield change
        for pub in set(pubmap1.keys()).difference(set(pubmap2.keys())):
            yield AssociationChange(
                publications=[pub],
                publication_is_deleted=True,
            )
        for pub in set(pubmap2.keys()).difference(set(pubmap1.keys())):
            yield AssociationChange(
                publications=[pub],
                publication_is_added=True,
            )

    def changes_by_primary_knowledge_source(
        self,
        assocs1: List[Association],
        assocs2: List[Association],
        predicates: List[PRED_CURIE],
    ) -> Iterator[AssociationChange]:
        """
        Perform diff on two association collections.

        :param assocs1:
        :param assocs2:
        :param predicates:
        :return:
        """
        map1 = pairs_as_dict(
            [(a.primary_knowledge_source, a) for a in assocs1 if a.primary_knowledge_source]
        )
        map2 = pairs_as_dict(
            [(a.primary_knowledge_source, a) for a in assocs2 if a.primary_knowledge_source]
        )
        in_common = set(map1.keys()).intersection(set(map2.keys()))
        for group in in_common:
            for change in self.calculate_change_objects(map1[group], map2[group], predicates):
                change.summary_group = group
                yield change

    @property
    def obsoletion_map(self):
        if self._obsoletion_map is None:
            obsoletes = list(self.adapter.obsoletes())
            self._obsoletion_map = {obs: [] for obs in obsoletes}
            for obs, _rel, replacement in self.adapter.obsoletes_migration_relationships(obsoletes):
                self._obsoletion_map[obs].append(replacement)
        return self._obsoletion_map
