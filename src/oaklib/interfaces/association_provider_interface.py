import logging
from abc import ABC
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from oaklib.datamodels.association import (
    Association,
    PairwiseCoAssociation,
    PositiveOrNegativeAssociation,
)
from oaklib.datamodels.similarity import TermSetPairwiseSimilarity
from oaklib.interfaces import MappingProviderInterface
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.associations.association_index import AssociationIndex
from oaklib.utilities.iterator_utils import chunk

ASSOCIATION_CORRELATION = Tuple[
    CURIE, CURIE, int, Optional[List[CURIE]], Optional[List[Association]]
]


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

    Associations (also known as annotations) connect data elements or entities to
    an ontology class. Examples of associations include:

    - Gene associations to terms in ontologies like GO, Mondo, Uberon, HPO, MPO, CL
    - Associations between spans of text and ontology entities

    Data models and file formats include:

    - The GO GAF and GPAD formats.
    - The HPOA association file format.
    - KGX (Knowledge Graph Exchange).
    - The W3 `Open Annotation <https://www.w3.org/TR/annotation-model/>`_ (OA) data model

    The OA datamodel considers an annotation to be between a *body* and a *target*:

    .. image:: https://www.w3.org/TR/annotation-vocab/images/examples/annotation.png

    .. warning::

        the signature of some methods are subject to change while we
        decide on the best patterns to define here.

    Note that most ontology sources are not themselves providers of associations; there is no agreed upon
    way to represent associations in OWL, and associations are typically distributed separately from
    ontologies. See the section :ref:`associations` in the OAK guide for more details.

    OAK provides a number of ways to augment an ontology adapter with associations.

    The most expressive way is to provide an :ref:`InputSpecification`:

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("src/oaklib/conf/go-pombase-input-spec.yaml")

    This combines an ontology source with one or more association sources.

    Another approach is to use an adapter that directly supports associations. An example of this
    is the :ref:`amigo_implementation`:

    >>> from oaklib import get_adapter
    >>> amigo = get_adapter("amigo:NCBITaxon:10090") # mouse




    Command Line Use
    ----------------

    .. code::

       runoak -i foo.db associations UBERON:0002101
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
        add_closure_fields: bool = False,
        **kwargs,
    ) -> Iterator[Association]:
        """
        Yield all matching associations.

        To query by subject (e.g. genes):

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("src/oaklib/conf/go-pombase-input-spec.yaml")
        >>> genes = ["PomBase:SPAC1142.02c", "PomBase:SPAC3H1.05", "PomBase:SPAC1142.06", "PomBase:SPAC4G8.02c"]
        >>> for assoc in adapter.associations(genes):
        ...    print(f"{assoc.object} {adapter.label(assoc.object)}")
        <BLANKLINE>
        ...
        GO:0006620 post-translational protein targeting to endoplasmic reticulum membrane
        ...

        To query by object (e.g. descriptor terms):

        >>> from oaklib import get_adapter
        >>> from oaklib.datamodels.vocabulary import IS_A, PART_OF
        >>> adapter = get_adapter("src/oaklib/conf/go-pombase-input-spec.yaml")
        >>> for assoc in adapter.associations(objects=["GO:0006620"], object_closure_predicates=[IS_A, PART_OF]):
        ...    print(f"{assoc.subject} {assoc.subject_label}")
        <BLANKLINE>
        ...
        PomBase:SPAC1142.02c sgt2
        ...

        When determining a match on `objects`, the predicates in ``object_closure_predicates`` is used.
        We recommend you always explicitly provide this. A good choice is typically IS_A and PART_OF for
        ontologies like GO, Uberon, CL, ENVO.

        :param subjects: constrain to these subjects (e.g. genes in a gene association)
        :param predicates: constrain to these predicates (e.g. involved-in for a gene to pathway association)
        :param objects: constrain to these objects (e.g. terms)
        :param property_filter: generic query filter
        :param subject_closure_predicates: subjects is treated as descendant via these predicates
        :param predicate_closure_predicates: predicates is treated as descendant via these predicates
        :param object_closure_predicates: object is treated as descendant via these predicates
        :param add_closure_fields: add subject and object closure fields to the association
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
            logging.info(f"No association index for {type(self)}")
            return
        yield from ix.lookup(subjects, predicates, objects)

    def _inject_subject_labels(self, association_iterator: Iterable[Association]):
        for assoc_it in chunk(association_iterator):
            associations = list(assoc_it)
            subjects = {a.subject for a in associations}
            label_map = {s: name for s, name in self.labels(subjects)}
            logging.info(f"LABEL MAP: {label_map} for {subjects}")
            for association in associations:
                if association.subject in label_map:
                    association.subject_label = label_map[association.subject]
            yield from associations

    def associations_subjects(self, *args, **kwargs) -> Iterator[CURIE]:
        """
        Yields all distinct subjects.

        >>> from oaklib import get_adapter
        >>> from oaklib.datamodels.vocabulary import IS_A, PART_OF
        >>> adapter = get_adapter("src/oaklib/conf/go-pombase-input-spec.yaml")
        >>> preds = [IS_A, PART_OF]
        >>> for gene in adapter.associations_subjects(objects=["GO:0045047"], object_closure_predicates=preds):
        ...    print(gene)
        <BLANKLINE>
        ...
        PomBase:SPBC1271.05c
        ...

        :param kwargs: same arguments as for :ref:`associations`
        :return:
        """
        # individual implementations should override this to be more efficient
        yielded = set()
        for a in self.associations(*args, **kwargs):
            s = a.subject
            if s in yielded:
                continue
            yield s
            yielded.add(s)

    def associations_subject_search(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        subject_prefixes: Optional[List[str]] = None,
        include_similarity_object: bool = False,
        method: Optional[str] = None,
        limit: Optional[int] = 10,
        sort_by_similarity: bool = True,
        **kwargs,
    ) -> Iterator[Tuple[float, Optional[TermSetPairwiseSimilarity], CURIE]]:
        """
        Search over all subjects in the association index.

        This relies on the SemanticSimilarityInterface.

        .. note::

           this is currently quite slow, this will be optimized in future

        :param subjects: optional set of subjects (e.g. genes) to search against
        :param predicates: only use associations with this predicate
        :param objects: this is the query - the asserted objects for all subjects
        :param property_filter: passed to associations query
        :param subject_closure_predicates: passed to associations query
        :param predicate_closure_predicates: passed to associations query
        :param object_closure_predicates: closure to use over the ontology
        :param subject_prefixes: only consider subjects with these prefixes
        :param include_similarity_object: include the similarity object in the result
        :param method: similarity method to use
        :param limit: max number of results to return
        :param kwargs:
        :return: iterator over ordered pairs of (score, sim, subject)
        """
        all_assocs = []
        if not subjects:
            all_assocs = list(
                self.associations(
                    predicates=predicates, subject_closure_predicates=subject_closure_predicates
                )
            )
            subjects = list({a.subject for a in all_assocs})
        rows = []
        n = 0
        for subject in subjects:
            if subject_prefixes:
                if not any(subject.startswith(prefix) for prefix in subject_prefixes):
                    continue
            if all_assocs:
                assocs = [a for a in all_assocs if a.subject == subject]
            else:
                assocs = self.associations(
                    subjects=[subject],
                    predicates=predicates,
                    property_filter=property_filter,
                    predicate_closure_predicates=predicate_closure_predicates,
                )
            terms = list({a.object for a in assocs})
            if not isinstance(self, SemanticSimilarityInterface):
                raise NotImplementedError
            sim = self.termset_pairwise_similarity(
                objects, terms, predicates=object_closure_predicates, labels=False
            )
            score = sim.best_score
            if include_similarity_object:
                row = (score, sim, subject)
            else:
                row = (score, None, subject)
            if sort_by_similarity:
                rows.append(row)
            else:
                yield row
                n += 1
                if limit and n >= limit:
                    break
        if rows:
            # sort each row tuple by the first element of the tuple
            n = 0
            for row in sorted(rows, key=lambda x: x[0], reverse=True):
                yield row
                n += 1
                if limit and n >= limit:
                    break

    def association_pairwise_coassociations(
        self,
        curies1: Iterable[CURIE],
        curies2: Iterable[CURIE],
        inputs_are_subjects=False,
        include_reciprocals=False,
        include_diagonal=True,
        include_entities=True,
        include_negated=False,
        **kwargs,
    ) -> Iterator[PairwiseCoAssociation]:
        """
        Find co-associations.

        >>> from oaklib import get_adapter
        >>> from oaklib.datamodels.vocabulary import IS_A, PART_OF
        >>> adapter = get_adapter("src/oaklib/conf/go-pombase-input-spec.yaml")
        >>> terms = ["GO:0000910", "GO:0006281", "GO:0006412"]
        >>> preds = [IS_A, PART_OF]
        >>> for coassoc in adapter.association_pairwise_coassociations(curies1=terms,
        ...                                              curies2=terms,
        ...                                              object_closure_predicates=preds):
        ...    print(coassoc.object1, coassoc.object2, coassoc.number_subjects_in_common)
        <BLANKLINE>
        ...
        GO:0006281 GO:0000910 0
        ...

        :param curies1:
        :param curies2:
        :param inputs_are_subjects:
        :param kwargs:
        :return:
        """
        if inputs_are_subjects:
            raise NotImplementedError
        curies1 = set(curies1)
        curies2 = set(curies2)
        symmetric = curies1 == curies2
        logging.info(f"Finding co-associations between {curies1} and {curies2}")

        def _filter_negated(
            assocs: Iterable[PositiveOrNegativeAssociation],
        ) -> List[PositiveOrNegativeAssociation]:
            if include_negated:
                return list(assocs)
            return [a for a in assocs if not a.negated]

        assocmap = {
            c: _filter_negated(self.associations(objects=[c], limit=-1, **kwargs))
            for c in curies1.union(curies2)
        }
        assocmap1 = {c: assocmap[c] for c in curies1}
        assocmap2 = {c: assocmap[c] for c in curies2}
        for c1 in curies1:
            for c2 in curies2:
                if c2 > c1 and not include_reciprocals and symmetric:
                    continue
                if c1 == c2 and not include_diagonal:
                    continue
                assocs1 = assocmap1[c1]
                assocs2 = assocmap2[c2]
                elements1 = {a.subject for a in assocs1}
                elements2 = {a.subject for a in assocs2}
                if not elements1 or not elements2:
                    logging.debug(
                        f"No associations for {c1} or {c2}, so a coassociation is not meaningful"
                    )
                    continue
                common = elements1.intersection(elements2)
                assocs_to_common = [a for a in assocs1 + assocs2 if a.subject in common]
                coassoc = PairwiseCoAssociation(
                    object1=c1,
                    object2=c2,
                    number_subjects_in_common=len(common),
                    number_subjects_in_union=len(elements1.union(elements2)),
                    number_subject_unique_to_entity1=len(elements1.difference(elements2)),
                    number_subject_unique_to_entity2=len(elements2.difference(elements1)),
                )
                if coassoc.number_subjects_in_union:
                    coassoc.proportion_subjects_in_common = (
                        coassoc.number_subjects_in_common / coassoc.number_subjects_in_union
                    )
                if elements1:
                    coassoc.proportion_entity1_subjects_in_entity2 = (
                        coassoc.number_subjects_in_common / len(elements1)
                    )
                if elements2:
                    coassoc.proportion_entity2_subjects_in_entity1 = (
                        coassoc.number_subjects_in_common / len(elements2)
                    )
                if include_entities:
                    coassoc.subjects_in_common = list(common)
                    coassoc.associations_for_subjects_in_common = assocs_to_common
                yield coassoc

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

    def association_counts(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
        group_by: Optional[str] = "object",
        limit: Optional[int] = None,
        **kwargs,
    ) -> Iterator[Tuple[CURIE, int]]:
        """
        Yield objects together with the number of distinct associations.

        :param subjects:
        :param predicates:
        :param property_filter:
        :param subject_closure_predicates:
        :param predicate_closure_predicates:
        :param object_closure_predicates:
        :param include_modified:
        :param group_by:
        :param limit:
        :param kwargs:
        :return:
        """
        association_it = self.associations(
            subjects=subjects,
            predicates=predicates,
            property_filter=property_filter,
            subject_closure_predicates=subject_closure_predicates,
            predicate_closure_predicates=predicate_closure_predicates,
            include_modified=include_modified,
            **kwargs,
        )
        assoc_map = defaultdict(list)
        cached = {}
        if not isinstance(self, OboGraphInterface):
            raise ValueError("This method requires an OboGraphInterface")
        for association in association_it:
            if group_by == "object":
                grp = association.object
                if grp not in cached:
                    grps = list(self.ancestors([grp], predicates=object_closure_predicates))
                    cached[grp] = grps
                else:
                    grps = cached[grp]
            elif group_by == "subject":
                grps = [association.subject]
            else:
                raise ValueError(f"Unknown group_by: {group_by}")
            for grp in grps:
                assoc_map[grp].append(association)
        for k, v in assoc_map.items():
            yield k, len(v)

    def association_subject_counts(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
        **kwargs,
    ) -> Iterator[Tuple[CURIE, int]]:
        """
        Yield objects together with the number of distinct associated subjects.

        Here objects are typically nodes from ontologies and subjects are annotated
        entities such as genes.

        >>> from oaklib import get_adapter
        >>> from oaklib.datamodels.vocabulary import IS_A, PART_OF
        >>> adapter = get_adapter("src/oaklib/conf/go-pombase-input-spec.yaml")
        >>> genes = ["PomBase:SPAC1142.02c", "PomBase:SPAC3H1.05", "PomBase:SPAC1142.06"]
        >>> preds = [IS_A, PART_OF]
        >>> for term, num in adapter.association_subject_counts(genes, object_closure_predicates=preds):
        ...    print(term, num)
        <BLANKLINE>
        ...
        GO:0051668 3
        ...

        This shows that GO:0051668 (localization within membrane) is used for all 3 input subjects.
        If subjects is empty, this is calculated for all subjects in the association set.

        :param subjects: constrain to these subjects (e.g. genes in a gene association)
        :param predicates: constrain to these predicates (e.g. involved-in for a gene to pathway association)
        :param property_filter: generic filter
        :param subject_closure_predicates: subjects is treated as descendant via these predicates
        :param predicate_closure_predicates: predicates is treated as descendant via these predicates
        :param object_closure_predicates: object is treated as descendant via these predicates
        :param include_modified: include modified associations
        :param kwargs: additional arguments
        :return:
        """
        association_it = self.associations(
            subjects=subjects,
            predicates=predicates,
            property_filter=property_filter,
            subject_closure_predicates=subject_closure_predicates,
            predicate_closure_predicates=predicate_closure_predicates,
            include_modified=include_modified,
            **kwargs,
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

        :param subjects: constrain to these subjects
        :param predicates: constrain to these predicates (e.g. involved-in for a gene to pathway association)
        :param objects: constrain to these objects (e.g. terms)
        :param subset: subset to map to
        :param subset_entities: subset entities to map to
        :param property_filter: generic filter
        :param subject_closure_predicates: subjects is treated as descendant via these predicates
        :param predicate_closure_predicates: predicates is treated as descendant via these predicates
        :param object_closure_predicates: object is treated as descendant via these predicates
        :param include_modified: include modified associations
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


@unique
class SubjectOrObjectRole(Enum):
    """
    Role of terms in the term list
    """

    SUBJECT = "subject"
    OBJECT = "object"
    BOTH = "both"
