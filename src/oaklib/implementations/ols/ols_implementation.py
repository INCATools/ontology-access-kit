from collections import ChainMap
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Iterable, Iterator, List, Optional, Tuple, Union
from urllib.parse import quote

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
from oaklib.interfaces.obograph_interface import GraphTraversalMethod
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


def _double_quote_iri(iri: str) -> str:
    """Double-encode an IRI for use in OLS4 term path segments.

    See: https://www.ebi.ac.uk/ols/docs/api
    """
    return quote(quote(iri, safe=""), safe="")


def _first_term(response: Any) -> Optional[Dict[str, Any]]:
    """Normalise an OLS ``get_term`` response down to a single term record.

    The OLS4 API (as returned by ``ols_client``) wraps term lookups in a
    paged/search-style payload of the form ``{"_embedded": {"terms": [...]}}``.
    Older/flat payloads that already look like a single term (i.e. contain a
    ``label`` key directly) are returned unchanged so this helper works across
    client versions.

    :param response: the raw response from ``client.get_term``
    :return: the first term record, or None if there are none
    """
    if not response:
        return None
    if isinstance(response, dict) and "_embedded" in response:
        terms = (response.get("_embedded") or {}).get("terms") or []
        return terms[0] if terms else None
    return response


def _scalar(value: Any) -> Optional[str]:
    """Coerce an OLS field to a scalar string.

    Some OLS4 fields (e.g. ``description``) are returned as lists; take the
    first non-empty element in that case.
    """
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        for item in value:
            if item:
                return item
        return None
    return value

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
        term = _first_term(self.client.get_term(ontology=ontology, iri=iri))
        if term:
            label = _scalar(term.get("label"))
            if label is not None:
                self.label_cache[curie] = label
                return label
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
        term = _first_term(self.client.get_term(ontology=ontology, iri=iri))
        if term:
            definition = _scalar(term.get("description"))
            if definition:
                self.definition_cache[curie] = definition
                return definition
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
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive: bool = True,
        method: Optional[GraphTraversalMethod] = None,
    ) -> Iterable[CURIE]:
        """
        Ancestors of the given term(s), as computed by the OLS hierarchy endpoints.

        The ``reflexive`` and ``method`` keywords are accepted for compatibility with
        the other graph adapters (see :class:`OboGraphInterface`).

        :param start_curies: curie or curies to start the walk from
        :param predicates: only traverse over these (traverses over all if this is not set)
        :param reflexive: include the start curie(s) in the result
        :param method: only the default (ENTAILMENT-style) traversal is supported
        :return: all ancestor CURIEs
        """
        if method is not None and method == GraphTraversalMethod.HOP:
            raise NotImplementedError("HOP traversal is not implemented for OLS")
        path_key = "hierarchicalAncestors"
        if predicates:
            if predicates == [IS_A]:
                path_key = "ancestors"
            elif IS_A not in predicates:
                raise NotImplementedError(f"OLS always include {IS_A}, you selected: {predicates}")
        start_curies = self._as_curie_list(start_curies)
        ancs = set()
        ontology = self.focus_ontology
        for curie in start_curies:
            iri = self.curie_to_uri(curie)
            path = f"ontologies/{ontology}/terms/{_double_quote_iri(iri)}/{path_key}"
            for record in self._iter_paged(path):
                obo_id = record.get("obo_id")
                if obo_id:
                    ancs.add(obo_id)
        if reflexive:
            ancs.update(start_curies)
        return list(ancs)

    def descendants(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: List[PRED_CURIE] = None,
        reflexive: bool = True,
        method: Optional[GraphTraversalMethod] = None,
    ) -> Iterable[CURIE]:
        """
        Descendants of the given term(s), backed by the OLS4 descendant endpoints.

        As with :meth:`ancestors`, OLS traversal always includes the ``is_a`` (subClassOf)
        relation, so ``predicates`` may either be omitted or must include ``rdfs:subClassOf``.

        :param start_curies: curie or curies to start the walk from
        :param predicates: only traverse over these (traverses over all if this is not set)
        :param reflexive: include the start curie(s) in the result
        :param method: only the default (ENTAILMENT-style) traversal is supported
        :return: all descendant CURIEs
        """
        if method is not None and method == GraphTraversalMethod.HOP:
            raise NotImplementedError("HOP traversal is not implemented for OLS")
        path_key = "hierarchicalDescendants"
        if predicates:
            if predicates == [IS_A]:
                path_key = "descendants"
            elif IS_A not in predicates:
                raise NotImplementedError(f"OLS always include {IS_A}, you selected: {predicates}")
        start_curies = self._as_curie_list(start_curies)
        descs = set()
        ontology = self.focus_ontology
        for curie in start_curies:
            iri = self.curie_to_uri(curie)
            path = f"ontologies/{ontology}/terms/{_double_quote_iri(iri)}/{path_key}"
            for record in self._iter_paged(path):
                obo_id = record.get("obo_id")
                if obo_id:
                    descs.add(obo_id)
        if reflexive:
            descs.update(start_curies)
        return list(descs)

    def _iter_paged(
        self, path: str, key: str = "terms", size: int = 500
    ) -> Iterator[Dict[str, Any]]:
        """Iterate over every record of a paged OLS4 collection endpoint.

        This walks the pages explicitly using the ``page``/``size`` query
        parameters and the ``page.totalPages`` field of the HAL response,
        rather than relying on ``ols_client.Client.get_paged``. That client
        helper looks for the *next* page under ``_links.href``, but OLS4 (like
        any HAL API) exposes it under ``_links.next.href``; the top-level key is
        never present, so the loop terminates after the first page and every
        result set is silently truncated to ``size`` (500) records. High-level
        terms such as ``GO:0005575`` (cellular_component) have thousands of
        descendants, so that truncation turns closure queries into silent false
        negatives. See https://github.com/ai4curation/ai-gene-review/issues/1653.

        :param path: the collection endpoint, relative to the API base URL
        :param key: the ``_embedded`` key to slice each page from
        :param size: the page size (OLS4 caps this at 500)
        :yields: every record across all pages
        """
        page = 0
        while True:
            response = self.client.get_json(path, params={"size": size, "page": page})
            embedded = (response or {}).get("_embedded") or {}
            records = embedded.get(key) or []
            yield from records
            page_info = (response or {}).get("page") or {}
            total_pages = page_info.get("totalPages")
            page += 1
            if not records:
                break
            if total_pages is not None and page >= total_pages:
                break

    @staticmethod
    def _as_curie_list(start_curies: Union[CURIE, List[CURIE]]) -> List[CURIE]:
        if isinstance(start_curies, str):
            return [start_curies]
        return list(start_curies)

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
