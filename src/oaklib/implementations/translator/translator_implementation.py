"""
Adapter for NCATS Biomedical Translator endpoints (experimental).

.. warning ::

    this is currently highly incomplete.
    Only NodeNormalizer API implemented so far

"""

import logging
from dataclasses import dataclass
from typing import Iterable, List, Mapping, Optional, Union

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
from oaklib.types import CURIE

__all__ = [
    "TranslatorImplementation",
]

from oaklib.utilities.mapping.sssom_utils import inject_mapping_sources

NODE_NORMALIZER_ENDPOINT = "https://nodenormalization-sri.renci.org/1.4/get_normalized_nodes"
NAME_NORMALIZER_ENDPOINT = "https://name-resolution-sri.renci.org"


@dataclass
class TranslatorImplementation(
    MappingProviderInterface,
    SearchInterface,
):
    """
    Wraps Translator endpoints.

    TODO: implement other endpoints
    """

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
            f"{NAME_NORMALIZER_ENDPOINT}/lookup",
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
            f"{NAME_NORMALIZER_ENDPOINT}/reverse_lookup",
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
            f"{NAME_NORMALIZER_ENDPOINT}/reverse_lookup",
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
