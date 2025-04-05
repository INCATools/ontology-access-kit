"""Adapter for AmiGO solr index."""

import json
import logging
import math
import re
from dataclasses import dataclass, field
from time import sleep
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

import pysolr

from oaklib.datamodels.association import Association, NegatedAssociation
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.vocabulary import IS_A, PART_OF, RDFS_LABEL, REGULATES, RELATED_TO
from oaklib.interfaces import OboGraphInterface, SearchInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)

__all__ = [
    "AmiGOImplementation",
]

from oaklib.interfaces.basic_ontology_interface import LANGUAGE_TAG, RELATIONSHIP
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.interfaces.usages_interface import UsagesInterface
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.iterator_utils import chunk

AMIGO_ENDPOINT = "http://golr.geneontology.org/solr/"

logger = logging.getLogger(__name__)

LIMIT = 10000

ONTOLOGY_CLASS_CATEGORY = "ontology_class"
BIOENTITY_CATEGORY = "ontology_class"

# TODO: derive from schema
DOCUMENT_CATEGORY = "document_category"
BIOENTITY = "bioentity"
BIOENTITY_LABEL = "bioentity_label"
ANNOTATION_CLASS = "annotation_class"
ANNOTATION_CLASS_LABEL = "annotation_class_label"
ISA_PARTOF_CLOSURE = "isa_partof_closure"
ISA_PARTOF_CLOSURE_LABEL = "isa_partof_closure_label"
REGULATES_CLOSURE = "regulates_closure"
REGULATES_CLOSURE_LABEL = "regulates_closure_label"
ISA_PARTOF_CLOSURE_PAIR = (ISA_PARTOF_CLOSURE, ISA_PARTOF_CLOSURE_LABEL)
REGULATES_CLOSURE_PAIR = (REGULATES_CLOSURE, REGULATES_CLOSURE_LABEL)
TAXON_CLOSURE = "taxon_closure"
ASSIGNED_BY = "assigned_by"
REFERENCE = "reference"
SUBSET = "subset"
QUALIFIER = "qualifier"
EVIDENCE_TYPE = "evidence_type"

NEIGHBORHOOD_GRAPH_JSON = "neighborhood_graph_json"
TOPOLOGY_GRAPH_JSON = "topology_graph_json"
REGULATES_TRANSITIVITY_GRAPH_JSON = "regulates_transitivity_graph_json"

# general
ENTITY = "entity"
ENTITY_LABEL = "entity_label"

DEFAULT_SELECT_FIELDS = [
    BIOENTITY,
    BIOENTITY_LABEL,
    ANNOTATION_CLASS,
    ANNOTATION_CLASS_LABEL,
    EVIDENCE_TYPE,
    QUALIFIER,
    ISA_PARTOF_CLOSURE,
    TAXON_CLOSURE,
    ASSIGNED_BY,
    REFERENCE,
]


def map_predicate(qualifiers: Iterable[str]) -> PRED_CURIE:
    for q in qualifiers:
        if q != "NOT":
            return f"biolink:{q.lower()}"
    return RELATED_TO


def _fq_element(k, vs):
    v = " OR ".join([f'"{v}"' for v in vs]) if isinstance(vs, list) else f'"{vs}"'
    return f"{k}:({v})"


def _query(
    solr, fq, fields=None, q=None, start: int = None, limit: int = None, **kwargs
) -> Iterator[Dict]:
    if start is None:
        start = 0
    if limit is None:
        limit = LIMIT
    fq_list = [_fq_element(k, vs) for k, vs in fq.items()]
    params = {"fq": fq_list, "fl": ",".join(fields), **kwargs}
    if not q:
        q = "*:*"
    logging.info(f"QUERY: {q} PARAMS: {params}")
    while True:
        results = solr.search(q, rows=limit, start=start, **params)
        yield from results
        logging.debug(f"CHECKING: {start} + {len(results)} >= {results.hits}")
        if start + len(results) >= results.hits:
            break
        else:
            start += limit
            sleep(0.1)


def _faceted_query(
    solr, fq, facet_field, fields=None, q=None, rows=0, facet_limit=10, min_facet_count=1, **kwargs
) -> Iterator[Tuple[str, int]]:
    fq_list = [_fq_element(k, vs) for k, vs in fq.items()]
    params = {
        "facet": "true",
        "fq": fq_list,
        "facet.field": facet_field,
        "facet.limit": facet_limit,
        "facet.mincount": min_facet_count,
        **kwargs,
    }
    if not q:
        q = "*:*"
    logging.info(f"QUERY: {q} PARAMS: {params}")
    results = solr.search(q, rows=rows, **params)
    ff = results.raw_response["facet_counts"]["facet_fields"][facet_field]
    for i in range(0, len(ff), 2):
        yield ff[i], ff[i + 1]


def _unnnormalize(curie: CURIE) -> CURIE:
    if curie.startswith("MGI:") and not curie.startswith("MGI:MGI:"):
        curie = f"MGI:{curie}"
    return curie


def _normalize(curie: CURIE) -> CURIE:
    if curie.startswith("MGI:MGI:"):
        curie = curie.replace("MGI:MGI:", "MGI:")
    return curie


@dataclass
class AmiGOImplementation(
    AssociationProviderInterface,
    OboGraphInterface,
    SearchInterface,
    UsagesInterface,
    SemanticSimilarityInterface,
):
    """
    Wraps AmiGO endpoint.

    The general form of the argument to :ref:`get_adapter()` is ``amigo:<NCBITaxonID>``:

    >>> from oaklib import get_adapter
    >>> amigo = get_adapter("amigo:NCBITaxon:9606")
    >>> gene_products = sorted([a.subject for a in amigo.associations(objects=["GO:0098794"])])
    >>> for gp in gene_products:
    ...     print(gp)
    <BLANKLINE>
    ...
    UniProtKB:P14867
    ...
    UniProtKB:P23677
    ...

    On the command line:

    .. code-block:: bash

        runoak -i amigo:NCBITaxon:9606 associations -p i,p GO:0098794



    """

    _solr: pysolr.Solr = None
    _source: str = None
    _go_adapter: OboGraphInterface = None
    _endpoint: str = field(default=AMIGO_ENDPOINT)

    def __post_init__(self):
        slug = self.resource.slug
        if slug:
            logger.info(f"Slug: {slug}")
            # e.g. amigo:{https://golr-staging.geneontology.io/solr/}:NCBITaxon:9606
            matches = re.match(r"^\{(\S+)\}:(.*)$", slug)
            if matches:
                logger.info(f"Looks like a specific endpoint is specified in {slug}")
                self._endpoint = matches.group(1)
                slug = matches.group(2)
        self._source = slug
        logger.info(f"Endpoint: {self._endpoint} Source: {self._source}")
        self._solr = pysolr.Solr(self._endpoint)

    def go_adapter(self) -> OboGraphInterface:
        if not self._go_adapter:
            from oaklib import get_adapter

            self._go_adapter = get_adapter("sqlite:obo:go")
        return self._go_adapter

    def _cache_nodes(self, nodes: List[Dict], curies: Iterable[CURIE]):
        for node in nodes:
            curie = node["id"]
            if curie in curies:
                lbl = node.get("lbl", None)
                if lbl:
                    self.property_cache.add(curie, RDFS_LABEL, node["lbl"])

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang:
            raise NotImplementedError
        if self.property_cache.contains(curie, RDFS_LABEL):
            return self.property_cache.get(curie, RDFS_LABEL)
        fq = {"document_category": ["general"], ENTITY: [curie]}
        solr = self._solr
        results = _query(solr, fq, [ENTITY_LABEL])
        self.property_cache.add(curie, RDFS_LABEL, None)
        for doc in results:
            lbl = doc[ENTITY_LABEL]
            self.property_cache.add(curie, RDFS_LABEL, lbl)
            return lbl

    def labels(
        self, curies: Iterable[CURIE], allow_none=True, lang: LANGUAGE_TAG = None
    ) -> Iterable[Tuple[CURIE, str]]:
        if lang:
            raise NotImplementedError
        # Note: some issues with post, use a low chunk size to ensure GET
        for curie_it in chunk(curies, 10):
            next_curies = list(curie_it)
            for curie in next_curies:
                lbl = self.property_cache.get(curie, RDFS_LABEL)
                if lbl is not None:
                    yield curie, lbl
                    next_curies.remove(curie)
            if not next_curies:
                continue
            fq = {"document_category": ["general"], ENTITY: next_curies}
            solr = self._solr
            results = _query(solr, fq, [ENTITY, ENTITY_LABEL])
            for doc in results:
                yield doc[ENTITY], doc[ENTITY_LABEL]

    def subset_members(self, subset: SUBSET_CURIE, **kwargs) -> Iterable[CURIE]:
        fq = {DOCUMENT_CATEGORY: [ONTOLOGY_CLASS_CATEGORY], SUBSET: [subset]}
        solr = self._solr
        results = _query(solr, fq, [ANNOTATION_CLASS])
        for doc in results:
            yield doc[ANNOTATION_CLASS]

    def _closure_fields(
        self, object_closure_predicates: Optional[List[PRED_CURIE]] = None
    ) -> Tuple[str, str]:
        if object_closure_predicates is None:
            return ISA_PARTOF_CLOSURE_PAIR
        if REGULATES in object_closure_predicates:
            return REGULATES_CLOSURE_PAIR
        if object_closure_predicates == [IS_A]:
            raise ValueError("object_closure_predicates must include IS_A and PART_OF")
        if not object_closure_predicates:
            return ANNOTATION_CLASS, ANNOTATION_CLASS_LABEL
        if not {IS_A, PART_OF, REGULATES}.intersection(object_closure_predicates):
            return ANNOTATION_CLASS, ANNOTATION_CLASS_LABEL
        return ISA_PARTOF_CLOSURE_PAIR

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
        solr = self._solr
        closure_field, closure_label_field = self._closure_fields(object_closure_predicates)
        # TODO: use _association_query
        fq = {DOCUMENT_CATEGORY: ["annotation"]}
        if subjects:
            subjects = [_unnnormalize(s) for s in subjects]
            fq[BIOENTITY] = subjects
        if objects:
            objects = list(objects)
            fq[closure_field] = objects
        if self._source:
            fq[TAXON_CLOSURE] = [self._source]

        select_fields = DEFAULT_SELECT_FIELDS
        if add_closure_fields:
            select_fields.append(closure_field)
            select_fields.append(closure_label_field)

        results = _query(solr, fq, select_fields)

        # fq_list = [_fq_element(k, vs) for k, vs in fq.items()]
        # params = {"fq": fq_list, "fl": ",".join(SELECT_FIELDS)}
        # results = solr.search("*:*", rows=1000, **params)
        for doc in results:
            cls = Association
            quals = set(doc.get(QUALIFIER, []))
            if "not" in quals:
                cls = NegatedAssociation
            assoc = cls(
                subject=_normalize(doc[BIOENTITY]),
                subject_label=doc[BIOENTITY_LABEL],
                predicate=map_predicate(quals),
                negated=cls == NegatedAssociation,
                object=doc[ANNOTATION_CLASS],
                object_label=doc[ANNOTATION_CLASS_LABEL],
                publications=doc[REFERENCE],
                evidence_type=doc.get(EVIDENCE_TYPE),
                primary_knowledge_source=doc[ASSIGNED_BY],
                aggregator_knowledge_source="infores:go",
            )
            if add_closure_fields:
                assoc.object_closure = doc[closure_field]
                assoc.object_closure_label = doc[closure_label_field]

            yield assoc

    def _association_query(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
        document_category: str = "annotation",
        **kwargs,
    ) -> Dict[str, Any]:
        closure_field, _ = self._closure_fields(object_closure_predicates)
        fq = {DOCUMENT_CATEGORY: [document_category]}
        if subjects:
            subjects = [_unnnormalize(s) for s in subjects]
            fq[BIOENTITY] = subjects
        if objects:
            objects = list(objects)
            fq[closure_field] = objects
        if self._source:
            fq[TAXON_CLOSURE] = [self._source]
        if property_filter:
            for k, v in property_filter.items():
                fq[k] = [v]
        return fq

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
        min_facet_count: Optional[int] = 1,
        **kwargs,
    ) -> Iterator[Tuple[CURIE, int]]:
        """
        Return the number of associations for each subject or object.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("amigo:NCBITaxon:9606")
        >>> for term, count in adapter.association_counts(group_by="object"):
        ...    print(f"Term: {term}  Approx Count: {int(count / 1000) * 1000)}")

        :param subjects:
        :param predicates:
        :param property_filter:
        :param subject_closure_predicates:
        :param predicate_closure_predicates:
        :param object_closure_predicates:
        :param include_modified:
        :param group_by:
        :param kwargs:
        :return:
        """
        closure_field, _ = self._closure_fields(object_closure_predicates)
        fq = self._association_query(
            subjects=subjects,
            predicates=predicates,
            property_filter=property_filter,
            subject_closure_predicates=subject_closure_predicates,
            predicate_closure_predicates=predicate_closure_predicates,
            object_closure_predicates=object_closure_predicates,
            include_modified=include_modified,
        )
        solr = self._solr
        if group_by == "object":
            if object_closure_predicates:
                if {IS_A, PART_OF}.difference(object_closure_predicates):
                    raise ValueError("object_closure_predicates must include IS_A and PART_OF")
                ff = closure_field
            else:
                ff = ANNOTATION_CLASS
        elif group_by == "subject":
            ff = BIOENTITY
        else:
            raise ValueError(f"Unknown group_by: {group_by}")
        yield from _faceted_query(
            solr, fq, facet_field=ff, rows=0, facet_limit=limit, min_facet_count=min_facet_count
        )

    # def association_pairwise_coassociations(
    #         self,
    #         curies1: Iterable[CURIE],
    #         curies2: Iterable[CURIE],
    #         inputs_are_subjects=False,
    #         include_reciprocals=False,
    #         include_diagonal=True,
    #         include_entities=True,
    #         **kwargs,
    # ) -> Iterator[PairwiseCoAssociation]:
    #     if include_entities or inputs_are_subjects:
    #         return super().association_pairwise_coassociations(
    #             curies1=curies1,
    #             curies2=curies2,
    #             inputs_are_subjects=inputs_are_subjects,
    #             include_reciprocals=include_reciprocals,
    #             include_diagonal=include_diagonal,
    #             include_entities=include_entities,
    #             **kwargs,
    #         )
    #     fq = {DOCUMENT_CATEGORY: ["annotation"]}
    #     if self._source:
    #         fq[TAXON_CLOSURE] = [self._source]
    #     params = {
    #         "facet": "true",
    #         "facet.field": BIOENTITY,
    #         "facet.limit": -1,
    #         "facet.mincount": 1,
    #     }
    #     params["facet.query"] = [f"{ISA_PARTOF_CLOSURE}:\"{c}\"" for c in curies1]
    #     solr = self._solr
    #     q = "*:*"
    #     fq_list = [_fq_element(k, vs) for k, vs in fq.items()]
    #     results = solr.search(q, rows=0, fq=fq_list, **params)
    #     print(results)
    #     ff = results.raw_response["facet_counts"]["facet_fields"][BIOENTITY]
    #     for i in range(0, len(ff), 2):
    #         yield ff[i], ff[i + 1]
    #

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
        raise NotImplementedError

    def relationships(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
    ) -> Iterator[RELATIONSHIP]:
        solr = self._solr
        fq = {DOCUMENT_CATEGORY: [ONTOLOGY_CLASS_CATEGORY]}
        # neighborhood graph is indexed for both subject and object
        if subjects:
            subjects = list(subjects)
            fq[ANNOTATION_CLASS] = subjects
        elif objects:
            objects = list(objects)
            fq[ANNOTATION_CLASS] = objects
        select_fields = [ANNOTATION_CLASS, NEIGHBORHOOD_GRAPH_JSON]
        if include_entailed:
            select_fields.append(REGULATES_TRANSITIVITY_GRAPH_JSON)
        results = _query(solr, fq, select_fields)

        for doc in results:
            neighborhood_graph = json.loads(doc[NEIGHBORHOOD_GRAPH_JSON])
            edges = neighborhood_graph["edges"]
            nodes = neighborhood_graph["nodes"]
            if include_entailed:
                closure_graph = json.loads(doc[REGULATES_TRANSITIVITY_GRAPH_JSON])
                edges.extend(closure_graph["edges"])
            if subjects:
                edges = [e for e in edges if e["sub"] in subjects]
            if objects:
                edges = [e for e in edges if e["obj"] in objects]
            if predicates:
                edges = [e for e in edges if e["pred"] in predicates]
            for edge in edges:
                s, p, o = edge["sub"], edge["pred"], edge["obj"]
                self._cache_nodes(nodes, [s, p, o])
                yield s, p, o

    def basic_search(
        self, search_term: str, config: Optional[SearchConfiguration] = None
    ) -> Iterable[CURIE]:
        solr = self._solr
        fq = {DOCUMENT_CATEGORY: ["general"]}
        # fq["general_blob"] = search_term
        results = _query(
            solr, fq, ["entity"], q=search_term, qf="general_blob_searchable", defType="edismax"
        )

        for doc in results:
            yield doc["entity"]

    def information_content_scores(
        self,
        curies: Optional[Iterable[CURIE]] = None,
        predicates: List[PRED_CURIE] = None,
        object_closure_predicates: List[PRED_CURIE] = None,
        use_associations: bool = None,
        term_to_entities_map: Dict[CURIE, List[CURIE]] = None,
        **kwargs,
    ) -> Iterator[Tuple[CURIE, float]]:
        closure_field, _ = self._closure_fields(object_closure_predicates)
        if curies and not isinstance(curies, list):
            curies = list(curies)
        fq = self._association_query(
            predicates=predicates,
            object_closure_predicates=object_closure_predicates,
            # objects=curies,
            document_category="bioentity",
        )
        solr = self._solr
        n_bioentities = None
        for term, count in _faceted_query(
            solr,
            fq,
            facet_field=DOCUMENT_CATEGORY,
            rows=0,
            facet_limit=-1,
            min_facet_count=1,
            **kwargs,
        ):
            if term == "bioentity":
                n_bioentities = count
        if n_bioentities is None:
            raise ValueError(f"No bioentities found in query {fq}")
        kwargs = {}
        # if curies:
        #    kwargs["facet.query"] = [_fq_element(ISA_PARTOF_CLOSURE, curie) for curie in curies]
        n = 0
        for term, count in _faceted_query(
            solr,
            fq,
            facet_field=closure_field,
            rows=0,
            facet_limit=-1,
            min_facet_count=1,
            **kwargs,
        ):
            n += 1
            if curies and term not in curies:
                continue
            ic = -math.log(count / n_bioentities) / math.log(2)
            yield term, ic

        logger.info(f"Iterated {n} counts")

    # delegation

    def descendants(
        self,
        *args,
        **kwargs,
    ) -> Iterable[CURIE]:
        yield from self.go_adapter().descendants(*args, **kwargs)

    def ancestors(
        self,
        *args,
        **kwargs,
    ) -> Iterable[CURIE]:
        yield from self.go_adapter().ancestors(*args, **kwargs)
