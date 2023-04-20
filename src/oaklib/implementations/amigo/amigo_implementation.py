"""
Adapter for AmiGO solr index.

.. warning ::

    this is currently highly incomplete.
    Only NodeNormalizer API implemented so far

"""
import logging
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional

import pysolr

from oaklib.datamodels.association import Association
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)

__all__ = [
    "AmiGOImplementation",
]

from oaklib.types import CURIE, PRED_CURIE

AMIGO_ENDPOINT = "http://golr.geneontology.org/solr/"

logger = logging.getLogger(__name__)

# TODO: derive from schema
BIOENTITY = "bioentity"
BIOENTITY_LABEL = "bioentity_label"
ANNOTATION_CLASS = "annotation_class"
ANNOTATION_CLASS_LABEL = "annotation_class_label"
ISA_PARTOF_CLOSURE = "isa_partof_closure"
TAXON_CLOSURE = "taxon_closure"
ASSIGNED_BY = "assigned_by"
REFERENCE = "reference"

SELECT_FIELDS = [
    BIOENTITY,
    BIOENTITY_LABEL,
    ANNOTATION_CLASS,
    ANNOTATION_CLASS_LABEL,
    ISA_PARTOF_CLOSURE,
    TAXON_CLOSURE,
    ASSIGNED_BY,
    REFERENCE,
]


@dataclass
class AmiGOImplementation(
    AssociationProviderInterface,
):
    """
    Wraps AmiGO endpoint.

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

    """

    _solr: pysolr.Solr = None
    _source: str = None

    def __post_init__(self):
        self._source = self.resource.slug
        self._solr = pysolr.Solr(AMIGO_ENDPOINT)

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
        solr = self._solr
        fq = {"document_category": ["annotation"]}
        if subjects:
            subjects = list(subjects)
            fq[BIOENTITY] = subjects
        if objects:
            objects = list(objects)
            fq[ISA_PARTOF_CLOSURE] = objects
        if self._source:
            fq[TAXON_CLOSURE] = [self._source]

        def _fq_element(k, vs):
            v = " OR ".join([f'"{v}"' for v in vs])
            return f"{k}:({v})"

        fq_list = [_fq_element(k, vs) for k, vs in fq.items()]
        params = {"fq": fq_list, "fl": ",".join(SELECT_FIELDS)}
        results = solr.search("*:*", rows=1000, **params)
        for doc in results:
            yield Association(
                subject=doc[BIOENTITY],
                subject_label=doc[BIOENTITY_LABEL],
                # predicate="",
                object=doc[ANNOTATION_CLASS],
                object_label=doc[ANNOTATION_CLASS_LABEL],
                publications=doc[REFERENCE],
                primary_knowledge_source=doc[ASSIGNED_BY],
                aggregator_knowledge_source="infores:go",
            )
