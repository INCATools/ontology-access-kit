"""Adapter for NCBIGene solr index."""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple
from xml.etree import ElementTree  # noqa S405

import requests

from oaklib.constants import TIMEOUT_SECONDS
from oaklib.datamodels.association import Association, NegatedAssociation
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.vocabulary import RDFS_LABEL
from oaklib.implementations.ncbi.eutils_implementation import EUtilsImplementation
from oaklib.interfaces import SearchInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)

__all__ = [
    "NCBIGeneImplementation",
]

from oaklib.interfaces.basic_ontology_interface import LANGUAGE_TAG
from oaklib.types import CURIE, PRED_CURIE

EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ELINK_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"

logger = logging.getLogger(__name__)


@dataclass
class NCBIGeneImplementation(
    AssociationProviderInterface,
    EUtilsImplementation,
    SearchInterface,
):
    """
    Wraps NCBIGene endpoint.

    The general form of the argument to :ref:`get_adapter()` is ``NCBIGene:<NCBITaxonID>``:

    >>> from oaklib import get_adapter
    >>> NCBIGene = get_adapter("NCBIGene:NCBITaxon:9606")
    >>> gene_products = sorted([a.subject for a in NCBIGene.associations(objects=["GO:0098794"])])
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

    def __post_init__(self):
        self._source = self.resource.slug
        # self._solr = pysolr.Solr(NCBIGene_ENDPOINT)

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang:
            raise NotImplementedError
        for _, lbl in self.labels([curie]):
            return lbl

    def labels(
        self, curies: Iterable[CURIE], allow_none=True, lang: LANGUAGE_TAG = None
    ) -> Iterable[Tuple[CURIE, str]]:
        if lang:
            raise NotImplementedError
        for curie in curies:
            yield curie, self.property_cache.get(curie, RDFS_LABEL)

    def associations(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        **kwargs,
    ) -> Iterator[Association]:
        if subjects is not None:
            subjects = list(subjects)
        if predicates is not None:
            predicates = list(predicates)
        if objects is not None:
            objects = list(objects)
        # TODO: branch logic based on predicates if specified
        yield from self.go_associations(
            subjects=subjects, predicates=predicates, objects=objects, **kwargs
        )
        yield from self.pubmed_associations(
            subjects=subjects, predicates=predicates, objects=objects, **kwargs
        )

    def go_associations(
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
        Extracts GO associations from the NCBIGene database.

        :param subjects:
        :param predicates:
        :param objects:
        :param property_filter:
        :param subject_closure_predicates:
        :param predicate_closure_predicates:
        :param object_closure_predicates:
        :param include_modified:
        :param add_closure_fields:
        :param kwargs:
        :return:
        """
        logging.info(f"SUBJS: {subjects}")
        if subjects:
            subjects = list(subjects)
        if not subjects:
            raise ValueError("NCBIGene requires subjects to be specified")

        for subject in subjects:
            if subject.startswith("NCBIGene:"):
                gene_id = subject.split(":")[1]
            elif subject.isnumeric():
                gene_id = subject
            else:
                raise ValueError("NCBIGene requires subjects to be NCBIGene CURIEs or numbers")
            params = {
                "db": "gene",
                "id": gene_id,
                "retmode": "xml",
            }
            response = self.requests_session.get(EFETCH_URL, params, timeout=TIMEOUT_SECONDS)

            # Parsing the XML file
            root = ElementTree.fromstring(response.content)  # noqa S314

            yield from self._go_associations_from_xml(subject, root)

    def pubmed_associations(
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
        Extracts pubmed associations from the NCBIGene database.

        :param subjects:
        :param predicates:
        :param objects:
        :param property_filter:
        :param subject_closure_predicates:
        :param predicate_closure_predicates:
        :param object_closure_predicates:
        :param include_modified:
        :param add_closure_fields:
        :param kwargs:
        :return:
        """
        logging.info(f"SUBJS: {subjects}")
        if subjects:
            subjects = list(subjects)
        if not subjects:
            raise ValueError("NCBIGene requires subjects to be specified")

        for subject in subjects:
            if subject.startswith("NCBIGene:"):
                gene_id = subject.split(":")[1]
            elif subject.isnumeric():
                gene_id = subject
            else:
                raise ValueError("NCBIGene requires subjects to be NCBIGene CURIEs or numbers")
            params = {
                "dbfrom": "gene",  # Link from Gene database
                "db": "pubmed",  # Link to PubMed database
                "id": gene_id,  # Gene ID (as number)
                "linkname": "gene_pubmed",  # Predefined link name for gene to PubMed
            }
            response = requests.get(ELINK_URL, params, timeout=TIMEOUT_SECONDS)

            # Parsing the XML file
            root = ElementTree.fromstring(response.text)  # noqa S314
            pmids = [linksetdb.text for linksetdb in root.findall(".//Link/Id")]

            for pmid in pmids:
                yield Association(
                    subject=subject,
                    # subject_label=gene_symbol,
                    predicate="biolink:mentioned_by",
                    object=f"PMID:{pmid}",
                    # object_label=go_label,
                )

    def _go_associations_from_xml(self, subject, root):
        """
        Extracts associations from the XML file

        :param subject:
        :param root:
        :return:
        """
        gene_symbol = None
        for gene_ref in root.iter("Gene-ref_locus"):
            gene_symbol = gene_ref.text
            self.property_cache.add(subject, RDFS_LABEL, gene_ref.text)

        # Searching for GO annotations in the specified structure
        subpath = "Gene-commentary/Gene-commentary_comment"
        for gene_commentary in root.findall(
            f".//Entrezgene_properties/{subpath}/{subpath}/Gene-commentary"
        ):
            pmids = set()
            for pmid in gene_commentary.iter("PubMedId"):
                pmids.add(f"PMID:{pmid.text}")
            for gene_commentary_source in gene_commentary.iter("Gene-commentary_source"):
                for other_source in gene_commentary_source:
                    # Check if the source is a GO term
                    if other_source.find("Other-source_src/Dbtag/Dbtag_db") is not None:
                        db_tag = other_source.find("Other-source_src/Dbtag/Dbtag_db").text
                        if db_tag == "GO":  # Confirming it's a GO term
                            # Extracting the GO ID
                            go_id = other_source.find(
                                "Other-source_src/Dbtag/Dbtag_tag/Object-id/Object-id_id"
                            ).text
                            go_id = f"GO:{int(go_id):07d}"
                            go_label = other_source.find("Other-source_anchor").text
                            self.property_cache.add(go_id, RDFS_LABEL, go_label)
                            predicate = other_source.find("Other-source_pre-text").text
                            # Extracting the evidence type
                            evidence = other_source.find("Other-source_post-text").text
                            evidence = evidence.split(": ")[1]
                            # Adding the extracted information to the list
                            preds = predicate.split(" ")
                            main_predicate = preds[-1]
                            cls = Association
                            if len(preds) > 1:
                                if preds[0] == "NOT":
                                    cls = NegatedAssociation
                            assoc = cls(
                                subject=subject,
                                subject_label=gene_symbol,
                                predicate=f"biolink:{main_predicate}",
                                object=go_id,
                                object_label=go_label,
                                evidence_type=evidence,
                                # property_values=[evidence_obj],
                                publications=list(pmids),
                            )
                            yield assoc

    def basic_search(
        self, search_term: str, config: Optional[SearchConfiguration] = None
    ) -> Iterable[CURIE]:
        search_params = {
            "db": "gene",  # Database to search in
            "term": search_term,  # Gene name or symbol to search for
            "retmode": "json",  # Return mode
            "retmax": "10",  # Number of results to return (adjust as needed)
        }

        response = requests.get(ESEARCH_URL, params=search_params, timeout=TIMEOUT_SECONDS)
        if response.status_code != 200:
            raise Exception(f"Failed to search for gene '{search_term}'")

        # Parse the JSON response
        result = response.json()
        ids = result.get("esearchresult", {}).get("idlist", [])

        for id in ids:
            yield f"NCBIGene:{id}"
