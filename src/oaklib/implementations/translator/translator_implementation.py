"""
Adapter for NCATS Biomedical Translator endpoints (experimental).

.. warning ::

    this is currently highly incomplete.
    Only NodeNormalizer API implemented so far

"""

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
        if "detail" in results:
            if results["detail"] == "Not found.":
                return
        for curies, data in results.items():
            nc_data = non_conflated_results.get(curies, {})
            label = None
            for x in data["equivalent_identifiers"]:
                if x["identifier"] == curies:
                    label = x["label"]
            for x in data["equivalent_identifiers"]:
                pred = (
                    SKOS_EXACT_MATCH
                    if any(
                        x2["identifier"] == x["identifier"]
                        for x2 in nc_data["equivalent_identifiers"]
                    )
                    else SKOS_CLOSE_MATCH
                )
                m = sssom.Mapping(
                    subject_id=curies,
                    subject_label=label,
                    predicate_id=pred,
                    object_id=x["identifier"],
                    object_label=x.get("label", None),
                    mapping_justification=str(SEMAPV.ManualMappingCuration.value),
                )
                inject_mapping_sources(m)
                yield m

    def inject_mapping_labels(self, mappings: Iterable[Mapping]) -> None:
        return
