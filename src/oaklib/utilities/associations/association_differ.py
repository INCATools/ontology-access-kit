import logging
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from typing import Collection, Iterator, List, Mapping, Set, Tuple

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
        """
        Calculates diff between two association sets.

        :param assocs1: the old association set
        :param assocs2: the new association set
        :param predicates: closure predicates
        :return:
        """
        obsoletion_map = self.obsoletion_map
        subject_map1 = pairs_as_dict([(a.subject, a) for a in assocs1])
        subject_map2 = pairs_as_dict([(a.subject, a) for a in assocs2])
        entities1 = set(subject_map1.keys())
        entities2 = set(subject_map2.keys())

        def _count_closure(o: CURIE, bg: Collection[CURIE]) -> int:
            if o in bg:
                return 0
            bg_closure = self.adapter.ancestors(list(bg), predicates)
            diff = set(self.adapter.ancestors([o], predicates)).difference(bg_closure)
            return len(diff)

        for entity in entities2.difference(entities1):
            objects1 = set([a.object for a in subject_map1[entity]])
            for a in subject_map2[entity]:
                yield AssociationChange(
                    subject=a.subject,
                    new_object=a.object,
                    is_creation=True,
                    closure_delta=_count_closure(a.object, objects1),
                )
        for entity in entities1.difference(entities2):
            objects2 = set([a.object for a in subject_map2[entity]])
            for a in subject_map1[entity]:
                yield AssociationChange(
                    subject=a.subject,
                    old_object=a.object,
                    is_deletion=True,
                    closure_delta=-_count_closure(a.object, objects2),
                )
        for entity in entities1.intersection(entities2):
            objects1 = set([a.object for a in subject_map1[entity]])
            objects2 = set([a.object for a in subject_map2[entity]])
            common = objects1.intersection(objects2)
            accounted_for_in_objects2 = set()
            for o in objects1.difference(objects2):
                logging.debug(f"Trying to account for {o} (unique to old) in {entity}")
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
                                closure_predicates=predicates,
                                closure_delta=0,
                            )
                    continue
                if not predicates:
                    yield AssociationChange(
                        subject=entity,
                        old_object=o,
                        is_deletion=True,
                        old_object_obsolete=old_object_obsolete,
                        closure_predicates=[],
                        closure_delta=-1,
                    )
                    continue
                o_ancestors = list(
                    self.adapter.ancestors([o], predicates=predicates, reflexive=True)
                )
                # candidate generalizations: any ancestor of o that is
                # not accounted for in the common set
                ixn = objects2.intersection(o_ancestors).difference(common)
                if ixn:
                    o2 = ixn.pop()
                    accounted_for_in_objects2.add(o2)
                    all_o2_ancestors = list(self.adapter.ancestors(list(objects2), predicates))
                    yield AssociationChange(
                        subject=entity,
                        old_object=o,
                        new_object=o2,
                        is_generalization=True,
                        old_object_obsolete=old_object_obsolete,
                        closure_predicates=predicates,
                        closure_delta=-_count_closure(o, all_o2_ancestors),
                    )
                    continue
                # detect specializations, where o becomes a descendant of o
                # ancestors of all in new
                o2_ancestors_of_unique = list(
                    self.adapter.ancestors(
                        list(objects2.difference(objects1)), predicates=predicates, reflexive=True
                    )
                )
                # o_descendants = list(
                #    self.adapter.descendants([o], predicates=predicates, reflexive=True)
                # )
                # ixn = objects2.intersection(o_descendants)
                if o in o2_ancestors_of_unique:
                    all_o1_ancestors = list(self.adapter.ancestors(list(objects1), predicates))
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
                        closure_delta=_count_closure(new_object, all_o1_ancestors),
                    )
                    continue
                # neither specialization nor generalization
                yield AssociationChange(
                    subject=entity,
                    old_object=o,
                    is_deletion=True,
                    old_object_obsolete=old_object_obsolete,
                    closure_predicates=predicates,
                    closure_delta=-_count_closure(o, objects2),
                )
            for o in objects2.difference(objects1):
                if o in accounted_for_in_objects2:
                    continue
                yield AssociationChange(
                    subject=entity,
                    new_object=o,
                    is_creation=True,
                    closure_predicates=predicates,
                    closure_delta=_count_closure(o, objects1),
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
            for assoc in pubmap1[pub]:
                yield AssociationChange(
                    publications=[pub],
                    publication_is_deleted=True,
                    subject=assoc.subject,
                    old_object=assoc.object,
                    old_object_obsolete=assoc.object in self.obsoletion_map,
                )
        for pub in set(pubmap2.keys()).difference(set(pubmap1.keys())):
            for assoc in pubmap1[pub]:
                yield AssociationChange(
                    publications=[pub],
                    publication_is_added=True,
                    subject=assoc.subject,
                    new_object=assoc.object,
                )
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
