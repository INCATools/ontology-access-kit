"""Adapter for AmiGO solr index."""
import logging
from dataclasses import dataclass
from time import sleep
from typing import Any, Dict, Iterable, Iterator, List, Optional

import pysolr

from oaklib.datamodels.association import Association
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)

__all__ = [
    "AmiGOImplementation",
]

from oaklib.interfaces.basic_ontology_interface import LANGUAGE_TAG
from oaklib.types import CURIE, PRED_CURIE

AMIGO_ENDPOINT = "http://golr.geneontology.org/solr/"

logger = logging.getLogger(__name__)

LIMIT = 10000

# TODO: derive from schema
DOCUMENT_CATEGORY = "document_category"
BIOENTITY = "bioentity"
BIOENTITY_LABEL = "bioentity_label"
ANNOTATION_CLASS = "annotation_class"
ANNOTATION_CLASS_LABEL = "annotation_class_label"
ISA_PARTOF_CLOSURE = "isa_partof_closure"
ISA_PARTOF_CLOSURE_LABEL = "isa_partof_closure_label"
TAXON_CLOSURE = "taxon_closure"
ASSIGNED_BY = "assigned_by"
REFERENCE = "reference"

# general
ENTITY = "entity"
ENTITY_LABEL = "entity_label"

DEFAULT_SELECT_FIELDS = [
    BIOENTITY,
    BIOENTITY_LABEL,
    ANNOTATION_CLASS,
    ANNOTATION_CLASS_LABEL,
    ISA_PARTOF_CLOSURE,
    TAXON_CLOSURE,
    ASSIGNED_BY,
    REFERENCE,
]


def _fq_element(k, vs):
    v = " OR ".join([f'"{v}"' for v in vs])
    return f"{k}:({v})"


def _query(solr, fq, fields, start: int = None, limit: int = None) -> Iterator[Dict]:
    if start is None:
        start = 0
    if limit is None:
        limit = LIMIT
    fq_list = [_fq_element(k, vs) for k, vs in fq.items()]
    params = {"fq": fq_list, "fl": ",".join(fields)}
    while True:
        results = solr.search("*:*", rows=limit, start=start, **params)
        yield from results
        logging.debug(f"CHECKING: {start} + {len(results)} >= {results.hits}")
        if start + len(results) >= results.hits:
            break
        else:
            start += limit
            sleep(0.1)


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



    """

    _solr: pysolr.Solr = None
    _source: str = None

    def __post_init__(self):
        self._source = self.resource.slug
        self._solr = pysolr.Solr(AMIGO_ENDPOINT)

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang:
            raise NotImplementedError
        fq = {"document_category": ["general"], ENTITY: [curie]}
        solr = self._solr
        results = _query(solr, fq, [ENTITY_LABEL])
        for doc in results:
            return doc[ENTITY_LABEL]

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
        fq = {DOCUMENT_CATEGORY: ["annotation"]}
        if subjects:
            subjects = [_unnnormalize(s) for s in subjects]
            fq[BIOENTITY] = subjects
        if objects:
            objects = list(objects)
            fq[ISA_PARTOF_CLOSURE] = objects
        if self._source:
            fq[TAXON_CLOSURE] = [self._source]

        select_fields = DEFAULT_SELECT_FIELDS
        if add_closure_fields:
            select_fields.append(ISA_PARTOF_CLOSURE)
            select_fields.append(ISA_PARTOF_CLOSURE_LABEL)

        results = _query(solr, fq, select_fields)

        # fq_list = [_fq_element(k, vs) for k, vs in fq.items()]
        # params = {"fq": fq_list, "fl": ",".join(SELECT_FIELDS)}
        # results = solr.search("*:*", rows=1000, **params)
        for doc in results:
            assoc = Association(
                subject=_normalize(doc[BIOENTITY]),
                subject_label=doc[BIOENTITY_LABEL],
                # predicate="",
                object=doc[ANNOTATION_CLASS],
                object_label=doc[ANNOTATION_CLASS_LABEL],
                publications=doc[REFERENCE],
                primary_knowledge_source=doc[ASSIGNED_BY],
                aggregator_knowledge_source="infores:go",
            )
            if add_closure_fields:
                assoc.subject_closure = doc[ISA_PARTOF_CLOSURE]
                assoc.subject_closure_label = doc[ISA_PARTOF_CLOSURE_LABEL]
            yield assoc
