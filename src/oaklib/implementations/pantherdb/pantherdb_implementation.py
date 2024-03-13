"""PantherDB implementation for OAK."""

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

import requests_cache
import sssom
from sssom.constants import SEMAPV
from sssom_schema import Mapping

from oaklib.datamodels.association import Association
from oaklib.datamodels.class_enrichment import ClassEnrichmentResult
from oaklib.datamodels.item_list import ItemList
from oaklib.datamodels.vocabulary import (
    BIOLOGICAL_PROCESS,
    CELLULAR_COMPONENT,
    MOLECULAR_FUNCTION,
    SKOS_EXACT_MATCH,
)
from oaklib.interfaces import (
    MappingProviderInterface,
    OboGraphInterface,
    SearchInterface,
)
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.class_enrichment_calculation_interface import (
    ClassEnrichmentCalculationInterface,
)
from oaklib.types import CURIE, PRED_CURIE

logger = logging.getLogger(__name__)


GENE_REQUESTS_CACHE = ".panther_requests_cache"


BASE_URL = "https://pantherdb.org/services/oai/pantherdb"


@dataclass
class PantherDBImplementation(
    ClassEnrichmentCalculationInterface,
    MappingProviderInterface,
    OboGraphInterface,
    AssociationProviderInterface,
    SearchInterface,
):
    """
    PantherDB implementation for OAK.

    This implementation provides access to PantherDB data and services.

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("pantherdb:9606")
    >>> for assoc in adapter.associations(["UniProtKB:P04217"]):
    ...     print(assoc.object)
    <BLANKLINE>
    ...
    GO:0005576
    ...

    In general this Adapter needs to be instantiated with a taxon_id,
    which is the NCBI Taxon ID for the species of interest.

    If your input IDs are all HGNC gene IDs, this is inferred automatically.

    Note that currently the PantherDB API doesn't distinguish between HGNC and NCBIGene IDs.
    Although you as the client will pass in CURIEs, only the numeric part is used, so matches
    may be more permissive than expected.

    """

    _requests_session: requests_cache.CachedSession = None

    requires_associations = False
    taxon_id: Optional[int] = None
    use_protein_ids: bool = True

    def __post_init__(self):
        slug = self.resource.slug
        if slug:
            slug = slug.replace("pantherdb:", "")
            self.taxon_id = int(slug)

    def requests_session(self):
        if self._requests_session is None:
            self._requests_session = requests_cache.CachedSession(GENE_REQUESTS_CACHE)
        return self._requests_session

    def _convert_gene_curies(
        self, curies: List[CURIE], expected_taxa: Optional[int] = None
    ) -> Dict[int, Dict[CURIE, str]]:
        taxon2ids = defaultdict(dict)
        for curie in curies:
            taxon_id = self.taxon_id
            [pfx, local_id] = curie.split(":")
            if pfx == "HGNC":
                taxon_id = 9606
            if not taxon_id:
                raise ValueError(f"Could not determine taxon for {curie}")
            taxon2ids[taxon_id][curie] = local_id
        if expected_taxa is not None:
            if len(taxon2ids) != expected_taxa:
                raise ValueError(f"Expected {expected_taxa} taxa, got {len(taxon2ids)}")
        return taxon2ids

    def _convert_gene_curies_single_taxon(
        self, curies: List[CURIE]
    ) -> Tuple[int, Dict[CURIE, str]]:
        taxon2ids = self._convert_gene_curies(curies, expected_taxa=1)
        taxon_id, id_pairs = list(taxon2ids.items())[0]
        return taxon_id, id_pairs

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
        **kwargs,
    ) -> Iterator[Association]:
        """
        Get associations from PantherDB.

        >>> from oaklib import get_adapter
        >>> adapter = get_adapter("pantherdb:9606")
        >>> for assoc in adapter.associations(["UniProtKB:P04217"]):
        ...     print(assoc.object)
        <BLANKLINE>
        ...
        GO:0005576
        ...

        :param subjects:
        :param predicates:
        :param objects:
        :param property_filter:
        :param subject_closure_predicates:
        :param predicate_closure_predicates:
        :param object_closure_predicates:
        :param include_modified:
        :param kwargs:
        :return:
        """
        if subjects and not isinstance(subjects, list):
            subjects = list(subjects)
        if objects and not isinstance(objects, list):
            objects = list(objects)
        if objects:
            raise ValueError("PantherDB does not support term-based queries")
        taxon2ids = self._convert_gene_curies(subjects)
        yield from self._functional_annotations(taxon2ids)
        yield from self._homologs(taxon2ids, homolog_type="O")

    def _curie_from_accession(self, gene: Union[Dict, str]):
        if isinstance(gene, str):
            acc = gene
        else:
            acc = gene["accession"]
        [sp, gene_curie, prot_curie] = acc.split("|")
        if self.use_protein_ids:
            return prot_curie.replace("=", ":")
        else:
            return gene_curie.replace("=", ":")

    def _functional_annotations(
        self,
        taxon2ids: Dict[int, Dict[CURIE, str]],
    ) -> Iterator[Association]:
        session = self.requests_session()
        for taxon_id, curie2id in taxon2ids.items():
            ids_str = ",".join(curie2id.values())
            r = session.get(
                f"{BASE_URL}/geneinfo", params={"geneInputList": ids_str, "organism": taxon_id}
            )
            r.raise_for_status()
            results = r.json()
            genes = results["search"]["mapped_genes"]["gene"]
            if not isinstance(genes, list):
                genes = [genes]
            for gene in genes:
                subject = self._curie_from_accession(gene)
                atl = gene["annotation_type_list"]
                content = atl.get("content", None)
                for adt in atl["annotation_data_type"]:
                    if "content" in adt:
                        content = adt["content"]
                    pfx = ""
                    if content == BIOLOGICAL_PROCESS:
                        predicate = "biolink:involved_in"
                    elif content == MOLECULAR_FUNCTION:
                        predicate = "biolink:has_function"
                    elif content == CELLULAR_COMPONENT:
                        predicate = "biolink:located_in"
                    elif content == "ANNOT_TYPE_ID_REACTOME_PATHWAY":
                        predicate = "biolink:involved_in"
                        pfx = "REACT:"
                    else:
                        continue
                    annlist = adt["annotation_list"]
                    anns = annlist["annotation"]
                    if not isinstance(anns, list):
                        anns = [anns]
                    for ann in anns:
                        obj = pfx + ann["id"]
                        yield Association(
                            subject=subject,
                            predicate=predicate,
                            object=obj,
                            object_label=ann["name"],
                        )

    def _homologs(
        self,
        taxon2ids: Dict[int, Dict[CURIE, str]],
        homolog_type: str = "O",
    ) -> Iterator[Association]:
        session = self.requests_session()
        for taxon_id, curie2id in taxon2ids.items():
            ids_str = ",".join(curie2id.values())
            r = session.get(
                f"{BASE_URL}/ortholog/matchortho",
                params={"geneInputList": ids_str, "organism": taxon_id},
            )
            r.raise_for_status()
            results = r.json()
            for m in results["search"]["mapping"]["mapped"]:
                subject = self._curie_from_accession(m["gene"])
                object = self._curie_from_accession(m["target_gene"])
                yield Association(
                    subject=subject,
                    predicate="biolink:homologous_to",
                    object=object,
                )

    def ontologies(self) -> Iterable[CURIE]:
        yield "infores:pantherdb"

    def sssom_mappings(
        self, curies: Optional[Union[CURIE, Iterable[CURIE]]] = None, source: Optional[str] = None
    ) -> Iterable[sssom.Mapping]:
        if isinstance(curies, CURIE):
            curies = [curies]
        else:
            curies = list(curies)
        session = self.requests_session()
        objects = set()
        subjects = set()
        taxon2ids = self._convert_gene_curies(curies)
        for taxon_id, curie2id in taxon2ids.items():
            ids_str = ",".join(curie2id.values())
            logger.info(f"Fetching mappings for {ids_str} in {taxon_id}")
            r = session.get(
                f"{BASE_URL}/geneinfo", params={"geneInputList": ids_str, "organism": taxon_id}
            )
            r.raise_for_status()
            results = r.json()
            logger.debug(f"Got results {results}")
            genes = results["search"]["mapped_genes"]["gene"]
            if not isinstance(genes, list):
                genes = [genes]
            for gene in genes:
                acc = gene["accession"]
                [sp, gene_curie, prot_curie] = acc.split("|")
                gene_curie = gene_curie.replace("=", ":")
                prot_curie = prot_curie.replace("=", ":")
                m = sssom.Mapping(
                    subject_id=gene_curie,
                    predicate_id=SKOS_EXACT_MATCH,
                    object_id=prot_curie,
                    mapping_justification=str(SEMAPV.ManualMappingCuration.value),
                )
                # inject_mapping_sources(m)
                logger.debug(f"Got mapping {m}")
                yield m
                subjects.add(gene_curie)
                objects.add(prot_curie)
        for curie in curies:
            if curie not in subjects:
                logging.warning(f"Could not find any mappings for {curie}")

    def inject_mapping_labels(self, mappings: Iterable[Mapping]) -> None:
        return

    def enriched_classes(
        self,
        subjects: Optional[Iterable[CURIE]] = None,
        item_list: Optional[ItemList] = None,
        predicates: Iterable[CURIE] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        background: Iterable[CURIE] = None,
        hypotheses: Iterable[CURIE] = None,
        cutoff=0.05,
        autolabel=False,
        filter_redundant=False,
        sort_by: str = None,
        direction="greater",
    ) -> Iterator[ClassEnrichmentResult]:
        if subjects and item_list:
            raise ValueError("Only one of subjects or item_list may be provided")
        if subjects is None:
            if not item_list:
                raise ValueError("Either subjects or item_list must be provided")
            if not item_list.itemListElements:
                raise ValueError("item_list must not be empty")
            subjects = item_list.itemListElements
        subjects = list(subjects)
        taxon_id, subject_idmap = self._convert_gene_curies_single_taxon(subjects)
        subject_ids_str = ",".join(subject_idmap.values())
        session = self.requests_session()
        r = session.get(
            f"{BASE_URL}/enrich/overrep",
            params={
                "geneInputList": subject_ids_str,
                "organism": taxon_id,
                "annotDataSet": "GO:0008150",
            },
        )
        r.raise_for_status()
        results = r.json()["results"]["result"]
        for result in results:
            if result["pValue"] > cutoff:
                break
            # TODO: all fields
            term = result["term"]
            yield ClassEnrichmentResult(
                class_id=term["id"],
                class_label=term["label"],
                p_value=result["pValue"],
                false_discovery_rate=result["fdr"],
                sample_count=result["number_in_list"],
                background_count=result["number_in_reference"],
            )
