from collections import ChainMap
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Iterable, Iterator, List, Optional, Tuple, Union

import requests
from ols_client import Client, EBIClient, TIBClient
from sssom_schema import Mapping

from oaklib.constants import TIMEOUT_SECONDS
from oaklib.datamodels import oxo
from oaklib.datamodels.oxo import ScopeEnum
from oaklib.datamodels.search import SearchConfiguration, SearchProperty
from oaklib.datamodels.text_annotator import TextAnnotation
from oaklib.datamodels.vocabulary import IS_A, SEMAPV
from oaklib.implementations.ols.constants import SEARCH_CONFIG
from oaklib.implementations.ols.oxo_utils import load_oxo_payload
from oaklib.interfaces.basic_ontology_interface import PREFIX_MAP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.types import CURIE, LANGUAGE_TAG, PRED_CURIE

__all__ = [
    # Abstract classes
    "BaseOlsImplementation",
    # Concrete classes
    "OlsImplementation",
    "TIBOlsImplementation",
]

ANNOTATION = Dict[str, Any]
SEARCH_ROWS = 50

oxo_pred_mappings = {
    ScopeEnum.EXACT.text: "skos:exactMatch",
    ScopeEnum.BROADER.text: "skos:broadMatch",
    ScopeEnum.NARROWER.text: "skos:narrowMatch",
    ScopeEnum.RELATED.text: "skos:closeMatch",
}


@dataclass
class BaseOlsImplementation(MappingProviderInterface, TextAnnotatorInterface, SearchInterface):
    """
    Implementation over OLS and OxO APIs
    """

    ols_client_class: ClassVar[type[Client]]
    label_cache: Dict[CURIE, str] = field(default_factory=lambda: {})
    definition_cache: Dict[CURIE, str] = field(default_factory=lambda: {})
    base_url = "https://www.ebi.ac.uk/spot/oxo/api/mappings"
    _prefix_map: Dict[str, str] = field(default_factory=lambda: {})
    focus_ontology: str = None
    client: Client = field(init=False)

    def __post_init__(self):
        self.client = self.ols_client_class()
        if self.focus_ontology is None:
            if self.resource:
                self.focus_ontology = self.resource.slug

    def add_prefix(self, curie: str, uri: str):
        [pfx, local] = curie.split(":", 1)
        if pfx not in self._prefix_map:
            self._prefix_map[pfx] = uri.replace(local, "")

    def prefix_map(self) -> PREFIX_MAP:
        return ChainMap(super().prefix_map(), self._prefix_map)

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        """
        Fetch the label for a CURIE from OLS.

        :param curie: The CURIE to fetch the label for
        :param lang: Optional language tag (not currently supported by this implementation)
        :return: The label for the CURIE, or None if not found
        """
        if curie in self.label_cache:
            return self.label_cache[curie]

        ontology = self.focus_ontology
        iri = self.curie_to_uri(curie)
        term = self.client.get_term(ontology=ontology, iri=iri)
        if term and "label" in term:
            self.label_cache[curie] = term["label"]
            return term["label"]
        return None

    def labels(
        self, curies: Iterable[CURIE], allow_none=True, lang: LANGUAGE_TAG = None
    ) -> Iterable[Tuple[CURIE, str]]:
        """
        Fetch labels for multiple CURIEs.

        :param curies: The CURIEs to fetch labels for
        :param allow_none: Whether to include CURIEs with no label
        :param lang: Optional language tag (not currently supported by this implementation)
        :return: Iterator of (CURIE, label) tuples
        """
        for curie in curies:
            label = self.label(curie, lang)
            if label is None and not allow_none:
                continue
            yield curie, label

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        """
        Fetch the definition for a CURIE from OLS.

        :param curie: The CURIE to fetch the definition for
        :param lang: Optional language tag (not currently supported by this implementation)
        :return: The definition for the CURIE, or None if not found
        """
        if curie in self.definition_cache:
            return self.definition_cache[curie]

        ontology = self.focus_ontology
        iri = self.curie_to_uri(curie)
        term = self.client.get_term(ontology=ontology, iri=iri)
        if term and "description" in term and term["description"]:
            self.definition_cache[curie] = term["description"]
            return term["description"]
        return None

    def definitions(
        self,
        curies: Iterable[CURIE],
        include_metadata=False,
        include_missing=False,
        lang: Optional[LANGUAGE_TAG] = None,
    ) -> Iterator[Tuple[CURIE, Optional[str], Dict]]:
        """
        Fetch definitions for multiple CURIEs from OLS.

        :param curies: The CURIEs to fetch definitions for
        :param include_metadata: Whether to include metadata (currently not supported)
        :param include_missing: Whether to include CURIEs with no definition
        :param lang: Optional language tag (not currently supported by this implementation)
        :return: Iterator of (CURIE, definition, metadata) tuples
        """
        for curie in curies:
            definition = self.definition(curie, lang)
            if definition is None and not include_missing:
                continue
            # Currently OLS doesn't provide metadata for definitions through the API
            # So we're just returning an empty dict
            yield curie, definition, {}

    def annotate_text(self, text: str) -> Iterator[TextAnnotation]:
        raise NotImplementedError

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def ancestors(
        self, start_curies: Union[CURIE, List[CURIE]], predicates: List[PRED_CURIE] = None
    ) -> Iterable[CURIE]:
        func = self.client.iter_hierarchical_ancestors
        if predicates:
            if predicates == [IS_A]:
                func = self.client.iter_ancestors
            elif IS_A not in predicates:
                raise NotImplementedError(f"OLS always include {IS_A}, you selected: {predicates}")
        if not isinstance(start_curies, list):
            start_curies = [start_curies]
        ancs = set()
        ontology = self.focus_ontology
        for curie in start_curies:
            iri = self.curie_to_uri(curie)
            records = func(ontology=ontology, iri=iri)
            ancs.update(record["obo_id"] for record in records)
        return list(ancs)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def basic_search(
        self, search_term: str, config: SearchConfiguration = SEARCH_CONFIG
    ) -> Iterable[CURIE]:
        query_fields = set()
        # Anything not covered by these conditions (i.e. query_fields set remains empty)
        # will cause the queryFields query param to be left off and all fields to be queried
        if SearchProperty(SearchProperty.IDENTIFIER) in config.properties:
            query_fields.update(["iri", "obo_id"])
        if SearchProperty(SearchProperty.LABEL) in config.properties:
            query_fields.update(["label"])
        if SearchProperty(SearchProperty.ALIAS) in config.properties:
            query_fields.update(["synonym"])
        if SearchProperty(SearchProperty.DEFINITION) in config.properties:
            query_fields.update(["description"])
        if SearchProperty(SearchProperty.INFORMATIVE_TEXT) in config.properties:
            query_fields.update(["description"])

        params = {
            "type": "class",
            "local": "true",
            "fieldList": "iri,label",
            "rows": config.limit if config.limit is not None else SEARCH_ROWS,
            "start": 0,
            "exact": (
                "true" if (config.is_complete is True or config.is_partial is False) else "false"
            ),
        }
        if len(query_fields) > 0:
            params["queryFields"] = ",".join(query_fields)
        if self.focus_ontology:
            params["ontology"] = self.focus_ontology.lower()

        for record in self.client.search(search_term, params=params):
            curie = self.uri_to_curie(record["iri"], strict=False)
            self.label_cache[curie] = record["label"]
            yield curie

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_sssom_mappings_by_curie(self, curie: Union[str, CURIE]) -> Iterator[Mapping]:
        result = requests.get(self.base_url, params=dict(fromId=curie), timeout=TIMEOUT_SECONDS)
        obj = result.json()
        container = load_oxo_payload(obj)
        return self.convert_payload(container)

    def convert_payload(self, container: oxo.Container) -> Iterator[Mapping]:
        oxo_mappings = container._embedded.mappings
        for oxo_mapping in oxo_mappings:
            oxo_s = oxo_mapping.fromTerm
            oxo_o = oxo_mapping.toTerm
            mapping = Mapping(
                subject_id=oxo_s.curie,
                subject_label=oxo_s.label,
                subject_source=oxo_s.datasource.prefix if oxo_s.datasource else None,
                predicate_id=oxo_pred_mappings[str(oxo_mapping.scope)],
                mapping_justification=SEMAPV.UnspecifiedMatching.value,
                object_id=oxo_o.curie,
                object_label=oxo_o.label,
                object_source=oxo_o.datasource.prefix if oxo_o.datasource else None,
                mapping_provider=oxo_mapping.datasource.prefix,
            )
            self.add_prefix(oxo_s.curie, oxo_s.uri)
            self.add_prefix(oxo_o.curie, oxo_o.uri)
            yield mapping

    # def fill_gaps(self, msdoc: MappingSetDocument, confidence: float = 1.0) -> int:
    #     curie_map = curie_to_uri_map(msdoc)
    #     # inv_map = {v: k for k, v in curie_map.items()}
    #     n = 0
    #     for curie, uri in curie_map.items():
    #         pfx, _ = curie.split(":", 2)
    #         ancs = self.get_ancestors(uri, ontology=pfx.lower())
    #         logging.debug(f"{curie} ANCS = {ancs}")
    #         for anc in ancs:
    #             if anc in curie_map:
    #                 m = Mapping(
    #                     subject_id=curie,
    #                     object_id=anc,
    #                     predicate_id="rdfs:subClassOf",
    #                     confidence=confidence,
    #                     match_type=MatchTypeEnum.HumanCurated,
    #                 )
    #                 logging.info(f"Gap filled link: {m}")
    #                 msdoc.mapping_set.mappings.append(m)
    #                 n += 1
    #     return n


class OlsImplementation(BaseOlsImplementation):
    """Implementation for the EBI OLS instance."""

    ols_client_class = EBIClient


class TIBOlsImplementation(BaseOlsImplementation):
    """Implementation for the TIB Hannover OLS instance."""

    ols_client_class = TIBClient
