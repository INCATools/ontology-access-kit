"""
Adapter for NCATS Biomedical Translator endpoints (experimental).

.. warning ::

    this is currently highly incomplete.
    Only NodeNormalizer API implemented so far

"""
import logging
from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Union

import requests
import sssom_schema.datamodel.sssom_schema as sssom

from oaklib.datamodels.vocabulary import SEMAPV, SKOS_CLOSE_MATCH, SKOS_EXACT_MATCH
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.types import CURIE

__all__ = [
    "TranslatorImplementation",
]

from oaklib.utilities.mapping.sssom_utils import inject_mapping_sources

NODE_NORMALIZER_ENDPOINT = "https://nodenormalization-sri.renci.org/1.3/get_normalized_nodes"


@dataclass
class TranslatorImplementation(
    MappingProviderInterface,
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
        r = requests.get(NODE_NORMALIZER_ENDPOINT, params={"curie": curies, "conflate": "false"})
        non_conflated_results = r.json()
        r = requests.get(NODE_NORMALIZER_ENDPOINT, params={"curie": curies, "conflate": "true"})
        results = r.json()
        objects = set()
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
                yield m
                objects.add(object_id)
        for curie in curies:
            if curie not in objects:
                logging.warning(f"Could not find any mappings for {curie}")

    def inject_mapping_labels(self, mappings: Iterable[Mapping]) -> None:
        return
