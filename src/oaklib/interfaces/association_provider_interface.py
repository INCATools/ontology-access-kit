from abc import ABC
from typing import Any, Dict, Iterable, Iterator, List, Optional

from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import ASSOCIATION, CURIE, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.associations.association_index import AssociationIndex


def associations_subjects(associations: Iterable[ASSOCIATION]) -> Iterator[CURIE]:
    """
    Yields distinct subjects for all associations.

    :param associations:
    :return:
    """
    seen = set()
    for a in associations:
        if a[0] in seen:
            continue
        yield a[0]
        seen.add(a[0])


def associations_objects(associations: Iterable[ASSOCIATION]) -> Iterator[CURIE]:
    """
    Yields distinct subjects for all associations.

    :param associations:
    :return:
    """
    seen = set()
    for a in associations:
        if a[2] in seen:
            continue
        yield a[2]
        seen.add(a[2])


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
    ) -> Iterator[ASSOCIATION]:
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

    def store_associations(self, associations: Iterable[ASSOCIATION]) -> bool:
        """

        :param associations:
        :return:
        """
        if self._association_index is None:
            self._association_index = AssociationIndex()
            self._association_index.create()
        self._association_index.populate(associations)
        return True

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
    ) -> Iterator[ASSOCIATION]:
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
                obj = association[2]
                ancs = list(self.ancestors([obj], predicates=object_closure_predicates))
                for mapped_obj in subset_entities.intersection(ancs):
                    association = association[0], association[1], mapped_obj, association[3]
                    yield association
