"""
Adapter for NCATS Biomedical Translator endpoints (experimental).

Provides wrappers for

- Node Normalization
- Name Resolution

Examples:

Name resolution:

    .. code-block:: bash

        runoak -i translator: info "citrate"
        CHEBI:16947 ! citrate(3-)
        CHEBI:31602 ! FENTANYL CITRATE
        CHEBI:30769 ! Citric acid
        CHEBI:64733 ! Potassium citrate
        CHEBI:131391 ! Magnesium citrate
        UNII:LXN6S3999X ! MAROPITANT CITRATE
        CHEBI:190513 ! Calcium citrate
        CHEBI:71197 ! TOFACITINIB CITRATE
        CHEBI:9139 ! Sildenafil
        CHEBI:3752 ! Clomifene


Aliases:

    .. code-block:: bash

        runoak -i translator: aliases "CHEBI:16947"
        curie	pred	alias
        CHEBI:16947	oio:hasRelatedSynonym	cit
        CHEBI:16947	oio:hasRelatedSynonym	Citrate
        CHEBI:16947	oio:hasRelatedSynonym	citrate
        CHEBI:16947	oio:hasRelatedSynonym	cit(3-)
        CHEBI:16947	oio:hasRelatedSynonym	citrate(3-)
        ...

Mappings:

    .. code-block:: bash

        runoak -i translator: mappings "CHEBI:16947" -O sssom
        # curie_map:
        #   CAS: http://w3id.org/sssom/unknown_prefix/cas/
        #   CHEBI: http://purl.obolibrary.org/obo/CHEBI_
        #   INCHIKEY: http://w3id.org/sssom/unknown_prefix/inchikey/
        #   PUBCHEM.COMPOUND: http://w3id.org/sssom/unknown_prefix/pubchem.compound/
        #   UNII: http://w3id.org/sssom/unknown_prefix/unii/
        #   owl: http://www.w3.org/2002/07/owl#
        #   rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
        #   rdfs: http://www.w3.org/2000/01/rdf-schema#
        #   semapv: https://w3id.org/semapv/vocab/
        #   skos: http://www.w3.org/2004/02/skos/core#
        #   sssom: https://w3id.org/sssom/
        # license: https://w3id.org/sssom/license/unspecified
        # mapping_set_id: https://w3id.org/sssom/mappings/6b8c0caf-98d7-4c08-b499-8922be3405db
        subject_id	subject_label	predicate_id	object_id
        CHEBI:16947	citrate(3-)	skos:exactMatch	CAS:126-44-3
        CHEBI:16947	citrate(3-)	skos:exactMatch	CHEBI:16947
        CHEBI:16947	citrate(3-)	skos:exactMatch	INCHIKEY:KRKNYBCHXYNGOX-UHFFFAOYSA-K
        CHEBI:16947	citrate(3-)	skos:exactMatch	PUBCHEM.COMPOUND:31348
        CHEBI:16947	citrate(3-)	skos:exactMatch	UNII:664CCH53PI

Term categories:

    .. code-block:: bash

        runoak -i translator: term-categories PUBCHEM.COMPOUND:31348
        curie	subset
        PUBCHEM.COMPOUND:31348	biolink:SmallMolecule
        PUBCHEM.COMPOUND:31348	biolink:MolecularEntity
        PUBCHEM.COMPOUND:31348	biolink:ChemicalEntity
        PUBCHEM.COMPOUND:31348	biolink:PhysicalEssence
        PUBCHEM.COMPOUND:31348	biolink:ChemicalOrDrugOrTreatment
        PUBCHEM.COMPOUND:31348	biolink:ChemicalEntityOrGeneOrGeneProduct
        PUBCHEM.COMPOUND:31348	biolink:ChemicalEntityOrProteinOrPolypeptide
        PUBCHEM.COMPOUND:31348	biolink:NamedThing
        PUBCHEM.COMPOUND:31348	biolink:PhysicalEssenceOrOccurrent


"""

import logging
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Mapping, Optional, Tuple, Union

import requests
import sssom_schema.datamodel.sssom_schema as sssom

from oaklib.constants import TIMEOUT_SECONDS
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.vocabulary import (
    HAS_RELATED_SYNONYM,
    RDFS_LABEL,
    SEMAPV,
    SKOS_CLOSE_MATCH,
    SKOS_EXACT_MATCH,
)
from oaklib.interfaces import SearchInterface
from oaklib.interfaces.basic_ontology_interface import ALIAS_MAP, LANGUAGE_TAG
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.semsim_interface import SemanticSimilarityInterface
from oaklib.types import CATEGORY_CURIE, CURIE, PRED_CURIE

__all__ = [
    "TranslatorImplementation",
]

from oaklib.utilities.mapping.sssom_utils import inject_mapping_sources

NODE_NORMALIZER_ENDPOINT = "https://nodenormalization-sri.renci.org/1.4/get_normalized_nodes"
NAME_RESOLUTION_ENDPOINT = "https://name-resolution-sri.renci.org"
ARS_SUBMIT_ENDPOINT = "https://ars-prod.transltr.io/ars/api/submit"


@dataclass
class TranslatorImplementation(
    MappingProviderInterface,
    SearchInterface,
    SemanticSimilarityInterface,
):
    """
    Wraps Translator SRI endpoints.
    """

    def terms_categories(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, CATEGORY_CURIE]]:
        if isinstance(curies, CURIE):
            curies = [curies]
        else:
            curies = list(curies)
        r = requests.get(
            NODE_NORMALIZER_ENDPOINT,
            params={"curie": curies, "conflate": "false"},
            timeout=TIMEOUT_SECONDS,
        )
        results = r.json()
        if "detail" in results:
            if results["detail"] == "Not found.":
                return
        for curie, data in results.items():
            for t in data.get("type", []):
                yield curie, t

    def information_content_scores(
        self,
        curies: Optional[Iterable[CURIE]] = None,
        predicates: List[PRED_CURIE] = None,
        object_closure_predicates: List[PRED_CURIE] = None,
        use_associations: bool = None,
        term_to_entities_map: Dict[CURIE, List[CURIE]] = None,
        **kwargs,
    ) -> Iterator[Tuple[CURIE, float]]:
        if isinstance(curies, CURIE):
            curies = [curies]
        else:
            curies = list(curies)
        r = requests.get(
            NODE_NORMALIZER_ENDPOINT,
            params={"curie": curies, "conflate": "false"},
            timeout=TIMEOUT_SECONDS,
        )
        results = r.json()
        if "detail" in results:
            if results["detail"] == "Not found.":
                return
        for curie, data in results.items():
            ic = data.get("information_content", None)
            if ic is not None:
                yield curie, ic

    def sssom_mappings(
        self, curies: Optional[Union[CURIE, Iterable[CURIE]]] = None, source: Optional[str] = None
    ) -> Iterable[Mapping]:
        if isinstance(curies, CURIE):
            curies = [curies]
        else:
            curies = list(curies)
        r = requests.get(
            NODE_NORMALIZER_ENDPOINT,
            params={"curie": curies, "conflate": "false"},
            timeout=TIMEOUT_SECONDS,
        )
        non_conflated_results = r.json()
        r = requests.get(
            NODE_NORMALIZER_ENDPOINT,
            params={"curie": curies, "conflate": "true"},
            timeout=TIMEOUT_SECONDS,
        )
        results = r.json()
        objects = set()
        subjects = set()
        if "detail" in results:
            if results["detail"] == "Not found.":
                return
        for curie, data in results.items():
            if not data:
                logging.info(f"No results for {curie} in {curies}")
                continue
            nc_data = non_conflated_results.get(curie, {})
            label = None
            equiv_identifiers = data.get("equivalent_identifiers", [])
            for x in equiv_identifiers:
                if x["identifier"] == curie:
                    label = x.get("label", None)
            for x in equiv_identifiers:
                object_id = x["identifier"]
                pred = (
                    SKOS_EXACT_MATCH
                    if any(
                        x2["identifier"] == object_id
                        for x2 in nc_data.get("equivalent_identifiers", [])
                    )
                    else SKOS_CLOSE_MATCH
                )
                m = sssom.Mapping(
                    subject_id=curie,
                    subject_label=label,
                    predicate_id=pred,
                    object_id=object_id,
                    object_label=x.get("label", None),
                    mapping_justification=str(SEMAPV.ManualMappingCuration.value),
                )
                inject_mapping_sources(m)
                if source:
                    if m.object_source != source:
                        continue
                yield m
                objects.add(object_id)
                subjects.add(curie)
        for curie in curies:
            if curie not in subjects:
                logging.warning(f"Could not find any mappings for {curie}")

    def inject_mapping_labels(self, mappings: Iterable[Mapping]) -> None:
        return

    def basic_search(
        self, search_term: str, config: Optional[SearchConfiguration] = None
    ) -> Iterable[CURIE]:
        r = requests.get(
            f"{NAME_RESOLUTION_ENDPOINT}/lookup",
            params={"string": search_term, "autocomplete": "true"},
            timeout=TIMEOUT_SECONDS,
        )
        r.raise_for_status()
        results = r.json()
        for result in results:
            curie = result["curie"]
            self.property_cache.add(curie, RDFS_LABEL, result["label"])
            yield curie

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang:
            raise NotImplementedError
        if self.property_cache.contains(curie, RDFS_LABEL):
            return self.property_cache.get(curie, RDFS_LABEL)
        r = requests.get(
            f"{NAME_RESOLUTION_ENDPOINT}/reverse_lookup",
            params={"curies": curie},
            timeout=TIMEOUT_SECONDS,
        )
        r.raise_for_status()
        results = r.json()
        if curie not in results:
            return None
        return results[curie]["preferred_name"]

    def entity_aliases(self, curie: CURIE) -> List[str]:
        r = requests.get(
            f"{NAME_RESOLUTION_ENDPOINT}/reverse_lookup",
            params={"curies": curie},
            timeout=TIMEOUT_SECONDS,
        )
        r.raise_for_status()
        results = r.json()
        if curie not in results:
            return []
        return results[curie]["names"]

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        return {HAS_RELATED_SYNONYM: self.entity_aliases(curie)}

    # def relationships(
    #         self,
    #         subjects: Iterable[CURIE] = None,
    #         predicates: Iterable[PRED_CURIE] = None,
    #         objects: Iterable[CURIE] = None,
    #         include_tbox: bool = True,
    #         include_abox: bool = True,
    #         include_entailed: bool = False,
    #         exclude_blank: bool = True,
    # ) -> Iterator[RELATIONSHIP]:
    #     query = {
    #         "message": {
    #             "query_graph": {
    #                 "edges": {
    #                     "e00": {
    #                         "subject": "n00",
    #                         "object": "n01",
    #                         "predicates": ["biolink:entity_negatively_regulates_entity"]
    #                     },
    #                     "e01": {
    #                         "subject": "n01",
    #                         "object": "n02",
    #                         "predicates": ["biolink:related_to"]
    #                     }
    #                 },
    #                 "nodes": {
    #                     "n00": {
    #                         "ids": ["PUBCHEM.COMPOUND:644073"],
    #                         "categories": ["biolink:ChemicalEntity"]
    #                     },
    #                     "n01": {
    #                         "categories": ["biolink:BiologicalProcessOrActivity", "biolink:Gene", "biolink:Pathway"]
    #                     },
    #                     "n02": {
    #                         "ids": ["HP:0000217"],
    #                         "categories": ["biolink:DiseaseOrPhenotypicFeature"]
    #                     }
    #                 }
    #             }
    #         }
    #     }
    #     r = requests.post(ARS_SUBMIT_ENDPOINT, json=query, timeout=TIMEOUT_SECONDS)
    #     pk = r.get('pk')
    #     import yaml
    #     print(yaml.dump(r.json()))
