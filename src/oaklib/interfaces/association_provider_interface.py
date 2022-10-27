from abc import ABC
from collections import defaultdict
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from oaklib.datamodels.association import Association
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.associations.association_index import AssociationIndex


def associations_subjects(associations: Iterable[Association]) -> Iterator[CURIE]:
    """
    Yields distinct subjects for all associations.

    :param associations:
    :return:
    """
    seen = set()
    for a in associations:
        if a.subject in seen:
            continue
        yield a.subject
        seen.add(a.subject)


def associations_objects(associations: Iterable[Association]) -> Iterator[CURIE]:
    """
    Yields distinct subjects for all associations.

    :param associations:
    :return:
    """
    seen = set()
    for a in associations:
        if a.object in seen:
            continue
        yield a.object
        seen.add(a.object)


class AssociationProviderInterface(BasicOntologyInterface, ABC):
    """
    An ontology provider that provides associations.
    """

    _association_index: AssociationIndex = None
    """In-memory index of associations"""

    def associations(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
    ) -> Iterator[Association]:
        """
        Yield all matching associations.

        :param subjects: constrain to these subjects (e.g. genes in a gene association)
        :param predicates: constrain to these predicates (e.g. involved-in for a gene to pathway association)
        :param objects: constrain to these objects (e.g. terms)
        :param property_filter: generic query filter
        :param subject_closure_predicates: subjects is treated as descendant via these predicates
        :param predicate_closure_predicates: predicates is treated as descendant via these predicates
        :param object_closure_predicates: object is treated as descendant via these predicates
        :param include_modified:
        :return:
        """
        # Default implementation: this may be overridden for efficiency
        if objects and object_closure_predicates:
            if isinstance(self, OboGraphInterface):
                # TODO: use more efficient procedure when object has many descendants
                objects = list(
                    self.descendants(list(objects), predicates=object_closure_predicates)
                )
            else:
                raise NotImplementedError
        ix = self._association_index
        for a in ix.lookup(subjects, predicates, objects):
            yield a

    def add_associations(self, associations: Iterable[Association]) -> bool:
        """
        Store a collection of associations for later retrievals.

        :param associations:
        :return:
        """
        if self._association_index is None:
            self._association_index = AssociationIndex()
            self._association_index.create()
        self._association_index.populate(associations)
        return True

    def association_subject_counts(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
    ) -> Iterator[Tuple[CURIE, int]]:
        """
        Yield objects together with the number of distinct associated subjects

        :param subjects:
        :param predicates:
        :param property_filter:
        :param subject_closure_predicates:
        :param predicate_closure_predicates:
        :param object_closure_predicates:
        :param include_modified:
        :return:
        """
        association_it = self.associations(
            subjects=subjects,
            predicates=predicates,
            property_filter=property_filter,
            subject_closure_predicates=subject_closure_predicates,
            predicate_closure_predicates=predicate_closure_predicates,
            include_modified=include_modified,
        )
        object_to_subject_map = defaultdict(set)
        if isinstance(self, OboGraphInterface):
            for association in association_it:
                subject = association.subject
                obj = association.object
                ancs = list(self.ancestors([obj], predicates=object_closure_predicates))
                for anc in ancs:
                    object_to_subject_map[anc].add(subject)
        for k, v in object_to_subject_map.items():
            yield k, len(v)

    def map_associations(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        subset: SUBSET_CURIE = None,
        subset_entities: Iterable[CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
    ) -> Iterator[Association]:
        # Default implementation: this may be overridden for efficiency
        if subset is None and subset_entities is None:
            raise ValueError("Must pass ONE OF subset OR subset_entities")
        if subset is not None and subset_entities is not None:
            raise ValueError("Must pass ONE OF subset OR subset_entities, not both")
        if subset:
            subset_entities = list(self.subset_members(subset))
        subset_entities = set(subset_entities)
        association_it = self.associations(
            subjects=subjects,
            predicates=predicates,
            property_filter=property_filter,
            subject_closure_predicates=subject_closure_predicates,
            predicate_closure_predicates=predicate_closure_predicates,
            include_modified=include_modified,
        )
        if isinstance(self, OboGraphInterface):
            for association in association_it:
                obj = association.object
                ancs = list(self.ancestors([obj], predicates=object_closure_predicates))
                for mapped_obj in subset_entities.intersection(ancs):
                    association = Association(
                        association.subject,
                        association.predicate,
                        mapped_obj,
                        property_values=association.property_values,
                    )
                    yield association
