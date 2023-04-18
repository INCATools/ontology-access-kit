import logging
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from oaklib.datamodels.association import Association
from oaklib.interfaces import MappingProviderInterface
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


@dataclass
class EntityNormalizer:
    """
    Describes how identifier fields should be normalized
    """

    adapter: MappingProviderInterface

    query_time: bool = field(default=False)
    strict: bool = field(default=False)

    source_prefixes: List[str] = field(default_factory=list)
    target_prefixes: List[str] = field(default_factory=list)

    prefix_alias_map: Dict[str, str] = field(default_factory=dict)

    slots: List[str] = field(default_factory=list)


@dataclass
class AssociationProviderInterface(BasicOntologyInterface, ABC):
    """
    An ontology provider that provides associations.
    """

    _association_index: AssociationIndex = None
    """In-memory index of associations"""

    normalizers: List[EntityNormalizer] = field(default_factory=list)

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

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("src/oaklib/conf/go-pombase-input-spec.yaml")
        >>> genes = ["PomBase:SPAC1142.02c", "PomBase:SPAC3H1.05", "PomBase:SPAC1142.06", "PomBase:SPAC4G8.02c"]
        >>> for assoc in adapter.associations(genes):
        ...    print(f"{assoc.object} {adapter.label(assoc.object)}")
        <BLANKLINE>
        ...
        GO:0006620 post-translational protein targeting to endoplasmic reticulum membrane
        ...

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
        if ix is None:
            logging.warning("No association index")
            return
        for a in ix.lookup(subjects, predicates, objects):
            yield a

    def add_associations(
        self,
        associations: Iterable[Association],
        normalizers: List[EntityNormalizer] = None,
        **kwargs,
    ) -> bool:
        """
        Store a collection of associations for later retrievals.

        :param associations:
        :param normalizers:
        :return:
        """
        if not normalizers and self.normalizers:
            normalizers = self.normalizers
        if normalizers:
            associations = list(associations)
            associations = self.normalize_associations(associations, normalizers)
        if self._association_index is None:
            logging.info("Creating association index")
            self._association_index = AssociationIndex()
            self._association_index.create()
        logging.info("Populating associations to index")
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
        Yield objects together with the number of distinct associated subjects.

        Here objects are typically nodes from ontologies and subjects are annotated
        entities such as genes.

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
        cached = {}
        if isinstance(self, OboGraphInterface):
            for association in association_it:
                subject = association.subject
                obj = association.object
                if obj not in cached:
                    ancs = list(self.ancestors([obj], predicates=object_closure_predicates))
                    cached[obj] = ancs
                else:
                    ancs = cached[obj]
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
        """
        Maps matching associations to a subset (map2slim, rollup).

        :param subjects:
        :param predicates:
        :param objects:
        :param subset:
        :param subset_entities:
        :param property_filter:
        :param subject_closure_predicates:
        :param predicate_closure_predicates:
        :param object_closure_predicates:
        :param include_modified:
        :return:
        """
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

    def normalize_associations(
        self,
        associations: Iterable[Association],
        normalizers: Optional[List[EntityNormalizer]] = None,
    ) -> Iterator[Association]:
        """
        Normalize associations.

        :param associations:
        :param normalizers:
        :return:
        """
        if not normalizers:
            return associations
        associations = list(associations)
        subject_ids = set([association.subject for association in associations])
        object_ids = set([association.object for association in associations])
        for normalizer in normalizers:
            if not normalizer.slots or "subject" in normalizer.slots:
                logging.info(f"Creating subject normalization map for {len(subject_ids)}")
                subject_nmap = normalizer.adapter.create_normalization_map(
                    subject_ids,
                    source_prefixes=normalizer.source_prefixes,
                    target_prefixes=normalizer.target_prefixes,
                    prefix_alias_map=normalizer.prefix_alias_map,
                )
                logging.info(f"Created subject normalization => {len(subject_nmap)}")
            else:
                subject_nmap = {}
            if not normalizer.slots or "object" in normalizer.slots:
                logging.info(f"Creating object normalization map for {len(object_ids)}")
                object_nmap = normalizer.adapter.create_normalization_map(
                    object_ids,
                    source_prefixes=normalizer.source_prefixes,
                    target_prefixes=normalizer.target_prefixes,
                )
            else:
                object_nmap = {}
            if subject_nmap or object_nmap:
                logging.info(
                    f"Normalizing associations using s: {len(subject_nmap)} o: {len(object_nmap)}"
                )
                for association in associations:
                    if association.subject in subject_nmap:
                        association.original_subject = association.subject
                        association.subject = subject_nmap[association.subject]
                    if association.object in object_nmap:
                        association.original_object = association.object
                        association.object = object_nmap[association.object]
        logging.info(f"Yielding {len(associations)} associations")
        yield from associations

    def normalize_association(
        self,
        association: Association,
        normalizers: Optional[List[EntityNormalizer]] = None,
    ) -> Association:
        """
        Normalize identifiers in an association.

        :param association:
        :param normalizers:
        :return:
        """
        if normalizers is None:
            return association
        for normalizer in normalizers:
            subject_prefix = association.subject.split(":")[0]
            object_prefix = association.object.split(":")[0]
            if subject_prefix in normalizer.source_prefixes:
                association.subject = normalizer.adapter.normalize(
                    association.subject,
                    target_prefixes=normalizer.target_prefixes,
                    strict=normalizer.strict,
                )
            if object_prefix in normalizer.source_prefixes:
                association.object = normalizer.adapter.normalize(
                    association.object,
                    target_prefixes=normalizer.target_prefixes,
                    strict=normalizer.strict,
                )
        return association
