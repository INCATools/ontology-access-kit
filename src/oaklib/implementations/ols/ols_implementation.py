import logging
from collections import ChainMap, defaultdict
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Iterable, Iterator, List, Optional, Tuple, Union
from urllib.parse import quote

import requests
from ols_client import Client, EBIClient, TIBClient
from sssom_schema import Mapping

from oaklib.constants import TIMEOUT_SECONDS
from oaklib.datamodels import obograph, oxo
from oaklib.datamodels.oxo import ScopeEnum
from oaklib.datamodels.search import SearchConfiguration, SearchProperty
from oaklib.datamodels.text_annotator import TextAnnotation
from oaklib.datamodels.vocabulary import (
    CONSIDER_REPLACEMENT,
    DEPRECATED_PREDICATE,
    HAS_DBXREF,
    HAS_DEFINITION_CURIE,
    HAS_OBO_NAMESPACE,
    HAS_OBSOLESCENCE_REASON,
    IN_SUBSET,
    IS_A,
    OIO_CREATED_BY,
    OIO_CREATION_DATE,
    OWL_ANNOTATION_PROPERTY,
    OWL_CLASS,
    OWL_NAMED_INDIVIDUAL,
    OWL_OBJECT_PROPERTY,
    PART_OF,
    RDFS_COMMENT,
    SCOPE_TO_SYNONYM_PRED_MAP,
    SEMAPV,
    TERM_REPLACED_BY,
)
from oaklib.implementations.ols.constants import SEARCH_CONFIG
from oaklib.implementations.ols.oxo_utils import load_oxo_payload
from oaklib.interfaces.basic_ontology_interface import ALIAS_MAP, PREFIX_MAP, RELATIONSHIP
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import GraphTraversalMethod, OboGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.types import CURIE, LANGUAGE_TAG, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.identifier_utils import synonym_type_code_from_curie
from oaklib.utilities.mapping.sssom_utils import inject_mapping_sources

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


def _xref_curie(xref: Any) -> Optional[CURIE]:
    """Turn an OLS xref record into a CURIE.

    OLS reports xrefs as ``{"database": "GOC", "id": "go_curators", ...}``; some
    payloads use flat strings instead.
    """
    if isinstance(xref, str):
        return xref or None
    if not isinstance(xref, dict):
        return None
    database = xref.get("database")
    identifier = xref.get("id")
    if database and identifier:
        return f"{database}:{identifier}"
    return identifier or None


def _synonym_predicate(scope: Optional[str]) -> PRED_CURIE:
    """Map an OLS synonym scope (e.g. ``hasNarrowSynonym``) onto a predicate CURIE."""
    if not scope:
        return "oio:hasExactSynonym"
    if ":" in scope:
        return scope
    return f"oio:{scope}"


def _is_uri(value: Any) -> bool:
    return isinstance(value, str) and (value.startswith("http://") or value.startswith("https://"))


def _is_annotation_property(record: Dict[str, Any]) -> bool:
    return bool(record.get("is_annotation_property")) or record.get("type") == "annotationProperty"


oxo_pred_mappings = {
    ScopeEnum.EXACT.text: "skos:exactMatch",
    ScopeEnum.BROADER.text: "skos:broadMatch",
    ScopeEnum.NARROWER.text: "skos:narrowMatch",
    ScopeEnum.RELATED.text: "skos:closeMatch",
}

#: OLS reports term annotations keyed by the *label* of the annotation property.
#: This maps the labels used by OBO ontologies onto the CURIEs used by OAK.
OLS_ANNOTATION_PREDICATES = {
    "comment": RDFS_COMMENT,
    "consider": CONSIDER_REPLACEMENT,
    "created_by": OIO_CREATED_BY,
    "creation_date": OIO_CREATION_DATE,
    "database_cross_reference": HAS_DBXREF,
    "has obsolescence reason": HAS_OBSOLESCENCE_REASON,
    "has_obo_namespace": HAS_OBO_NAMESPACE,
    "id": "oio:id",
    "term replaced by": TERM_REPLACED_BY,
}

logger = logging.getLogger(__name__)


@dataclass
class BaseOlsImplementation(
    MappingProviderInterface,
    OboGraphInterface,
    TextAnnotatorInterface,
    SearchInterface,
):
    """
    Implementation over OLS and OxO APIs
    """

    ols_client_class: ClassVar[type[Client]]
    label_cache: Dict[CURIE, Optional[str]] = field(default_factory=lambda: {})
    definition_cache: Dict[CURIE, Optional[str]] = field(default_factory=lambda: {})
    #: raw OLS term payloads, keyed by (curie, language tag). A single term lookup
    #: carries the label, definition, synonyms, xrefs, subsets and obsoletion status,
    #: so caching the payload means one HTTP round trip per term rather than one per
    #: property.
    term_cache: Dict[Tuple[CURIE, Optional[LANGUAGE_TAG]], Optional[Dict[str, Any]]] = field(
        default_factory=lambda: {}
    )
    owl_type_cache: Dict[CURIE, List[CURIE]] = field(default_factory=lambda: {})
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

    def term_metadata(
        self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch (and cache) the raw OLS payload describing a term.

        Every other lookup in this adapter is derived from this payload, so a term is
        only ever fetched once per language.

        :param curie: the CURIE to look up
        :param lang: optional language tag
        :return: the raw OLS record, or None if OLS has no such term
        """
        key = (curie, lang)
        if key in self.term_cache:
            return self.term_cache[key]
        ontology = self.focus_ontology
        iri = self.curie_to_uri(curie)
        try:
            if lang is None:
                response = self.client.get_term(ontology=ontology, iri=iri)
            else:
                response = self.client.get_json(
                    f"ontologies/{ontology}/terms", params={"iri": iri, "lang": lang}
                )
            term = _first_term(response)
        except requests.HTTPError as error:
            if error.response is None or error.response.status_code != requests.codes.not_found:
                raise
            # a confirmed 404 means the IRI is not a term in this ontology
            term = None
        self.term_cache[key] = term
        return term

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        """
        Fetch the label for a CURIE from OLS.

        :param curie: The CURIE to fetch the label for
        :param lang: Optional language tag; OLS serves translated labels where available
        :return: The label for the CURIE, or None if not found
        """
        if lang is None and curie in self.label_cache:
            return self.label_cache[curie]
        term = self.term_metadata(curie, lang=lang)
        label = _scalar(term.get("label")) if term else None
        if lang is None:
            self.label_cache[curie] = label
        return label

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
        if lang is None and curie in self.definition_cache:
            return self.definition_cache[curie]
        term = self.term_metadata(curie, lang=lang)
        definition = _scalar(term.get("description")) if term else None
        if not definition:
            definition = None
        if lang is None:
            self.definition_cache[curie] = definition
        return definition

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
        :param include_metadata: if True, include the xrefs supporting each definition
        :param include_missing: Whether to include CURIEs with no definition
        :param lang: Optional language tag
        :return: Iterator of (CURIE, definition, metadata) tuples
        """
        for curie in curies:
            definition = self.definition(curie, lang)
            if definition is None and not include_missing:
                continue
            metadata: Dict[PRED_CURIE, List[str]] = {}
            if include_metadata:
                xrefs = self._definition_xrefs(curie, lang=lang)
                if xrefs:
                    metadata[HAS_DBXREF] = xrefs
            yield curie, definition, metadata

    def _definition_xrefs(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> List[CURIE]:
        """Return the xrefs attached to a term's definition (``obo_definition_citation``)."""
        term = self.term_metadata(curie, lang=lang) or {}
        for citation in term.get("obo_definition_citation") or []:
            if not isinstance(citation, dict):
                continue
            return [
                xref
                for xref in (_xref_curie(x) for x in citation.get("oboXrefs") or [])
                if xref is not None
            ]
        return []

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: BasicOntologyInterface (aliases, metadata, subsets, types)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        """
        Return all labels and synonyms for a term, keyed by predicate.

        OLS reports the scope of each synonym in ``obo_synonym``; where an ontology has
        no OBO-style synonyms the flat ``synonyms`` list is used and every entry is
        reported as an exact synonym.
        """
        alias_map: ALIAS_MAP = defaultdict(list)
        term = self.term_metadata(curie) or {}
        label = _scalar(term.get("label"))
        if label:
            alias_map["rdfs:label"].append(label)
        for _, spv in self.synonym_property_values([curie]):
            alias_map[f"oio:{spv.pred}"].append(spv.val)
        return dict(alias_map)

    def synonym_property_values(
        self, subject: Union[CURIE, Iterable[CURIE]]
    ) -> Iterator[Tuple[CURIE, obograph.SynonymPropertyValue]]:
        """
        Yield the synonyms of a term, with scope, type and xrefs where OLS provides them.

        OLS exposes synonyms twice: a flat ``synonyms`` list and a richer
        ``obo_synonym`` list carrying scope and provenance. The two are not always in
        sync (exact synonyms are frequently missing from ``obo_synonym``), so both are
        merged here, with the richer record winning.
        """
        subjects = [subject] if isinstance(subject, str) else list(subject)
        for curie in subjects:
            term = self.term_metadata(curie) or {}
            seen = set()
            for synonym in term.get("obo_synonym") or []:
                if not isinstance(synonym, dict):
                    continue
                value = synonym.get("name")
                if not value:
                    continue
                seen.add(value)
                predicate = _synonym_predicate(synonym.get("scope"))
                spv = obograph.SynonymPropertyValue(pred=predicate.split(":")[-1], val=value)
                xrefs = [
                    xref
                    for xref in (_xref_curie(x) for x in synonym.get("xrefs") or [])
                    if xref is not None
                ]
                if xrefs:
                    spv.xrefs = xrefs
                synonym_type = synonym.get("type")
                if synonym_type:
                    if isinstance(synonym_type, list):
                        synonym_type = synonym_type[0]
                    spv.synonymType = synonym_type_code_from_curie(str(synonym_type))
                yield curie, spv
            for value in term.get("synonyms") or []:
                if value and value not in seen:
                    seen.add(value)
                    yield curie, obograph.SynonymPropertyValue(pred="hasExactSynonym", val=value)

    def entity_metadata_map(self, curie: CURIE) -> Dict[PRED_CURIE, List[str]]:
        """
        Return the metadata (annotation) statements OLS holds about a term.

        Structured OLS fields (definition, xrefs, subsets, obsoletion status) are
        reported under their standard CURIEs; free-form entries in the OLS
        ``annotation`` block are translated where the annotation property is known.
        """
        term = self.term_metadata(curie)
        if not term:
            return {}
        metadata_map: Dict[PRED_CURIE, List[str]] = defaultdict(list)
        definition = _scalar(term.get("description"))
        if definition:
            metadata_map[HAS_DEFINITION_CURIE].append(definition)
        for predicate, values in self.entity_alias_map(curie).items():
            metadata_map[predicate].extend(values)
        for xref in term.get("obo_xref") or []:
            curie_xref = _xref_curie(xref)
            if curie_xref is not None:
                metadata_map[HAS_DBXREF].append(curie_xref)
        for subset in term.get("in_subset") or []:
            metadata_map[IN_SUBSET].append(subset)
        if term.get("is_obsolete"):
            metadata_map[DEPRECATED_PREDICATE].append(True)
        for key, values in (term.get("annotation") or {}).items():
            predicate = OLS_ANNOTATION_PREDICATES.get(key)
            if predicate is None:
                logger.debug("No CURIE known for OLS annotation key %s", key)
                continue
            if predicate == HAS_DBXREF:
                # already covered by obo_xref, which is better structured
                continue
            for value in values if isinstance(values, list) else [values]:
                contracted = self.uri_to_curie(value, strict=False) if _is_uri(value) else value
                if contracted:
                    metadata_map[predicate].append(contracted)
        return {predicate: values for predicate, values in metadata_map.items() if values}

    def terms_subsets(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, SUBSET_CURIE]]:
        for curie in curies:
            term = self.term_metadata(curie) or {}
            for subset in term.get("in_subset") or []:
                yield curie, subset

    def owl_types(self, entities: Iterable[CURIE]) -> Iterable[Tuple[CURIE, CURIE]]:
        """
        Determine the OWL type of each entity.

        OLS serves classes, properties and individuals from separate endpoints, so the
        type is determined by looking the entity up in each in turn.
        """
        for curie in entities:
            for owl_type in self.owl_type(curie):
                yield curie, owl_type

    def owl_type(self, entity: CURIE) -> List[CURIE]:
        if entity in self.owl_type_cache:
            return self.owl_type_cache[entity]
        owl_types: List[CURIE] = []
        if self.term_metadata(entity) is not None:
            owl_types.append(OWL_CLASS)
        else:
            for path, owl_type in [
                ("properties", OWL_OBJECT_PROPERTY),
                ("individuals", OWL_NAMED_INDIVIDUAL),
            ]:
                record = self._lookup_non_class(entity, path)
                if record is None:
                    continue
                if path == "properties" and _is_annotation_property(record):
                    owl_types.append(OWL_ANNOTATION_PROPERTY)
                else:
                    owl_types.append(owl_type)
                break
        self.owl_type_cache[entity] = owl_types
        return owl_types

    def _lookup_non_class(self, curie: CURIE, path: str) -> Optional[Dict[str, Any]]:
        iri = self.curie_to_uri(curie)
        try:
            response = self.client.get_json(
                f"ontologies/{self.focus_ontology}/{path}", params={"iri": iri}
            )
        except requests.HTTPError as error:
            if error.response is None or error.response.status_code != requests.codes.not_found:
                raise
            return None
        records = ((response or {}).get("_embedded") or {}).get(path) or []
        return records[0] if records else None

    def defined_by(self, entity: CURIE) -> Optional[str]:
        term = self.term_metadata(entity)
        if term:
            prefix = term.get("ontology_prefix")
            if prefix:
                return prefix
        return super().defined_by(entity)

    def obsoletes(self, include_merged=True) -> Iterable[CURIE]:
        """
        Yield the obsolete terms in the focus ontology.

        .. warning::

            This walks every term in the ontology and is therefore slow for large
            ontologies.
        """
        for curie in self.entities(filter_obsoletes=False):
            term = self.term_metadata(curie)
            if not term or not term.get("is_obsolete"):
                continue
            if not include_merged:
                reasons = (term.get("annotation") or {}).get("has obsolescence reason") or []
                if any("IAO_0000227" in str(reason) for reason in reasons):
                    continue
            yield curie

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        """
        Yield every term in the focus ontology.

        .. warning::

            This pages through the whole ontology; for large ontologies such as
            ChEBI this is many thousands of HTTP requests.

        :param filter_obsoletes: exclude obsolete terms
        :param owl_type: restrict to this OWL type (only ``owl:Class`` is supported)
        :return: iterator over CURIEs
        """
        if owl_type is not None and owl_type != OWL_CLASS:
            raise NotImplementedError(f"OLS entities() only supports owl:Class, got {owl_type}")
        if not self.focus_ontology:
            raise ValueError("entities() requires a focus ontology, e.g. ols:go")
        seen = set()
        for record in self._iter_paged(f"ontologies/{self.focus_ontology}/terms"):
            curie = record.get("obo_id")
            if not curie:
                iri = record.get("iri")
                curie = self.uri_to_curie(iri, strict=False) if iri else None
            if not curie or curie in seen:
                continue
            seen.add(curie)
            if filter_obsoletes and record.get("is_obsolete"):
                continue
            # populate the cache so a follow-up label() lookup is free
            self.term_cache.setdefault((curie, None), record)
            yield curie

    def ontologies(self) -> Iterable[CURIE]:
        if self.focus_ontology:
            yield self.focus_ontology
            return
        for record in self._iter_paged("ontologies", key="ontologies"):
            ontology_id = record.get("ontologyId")
            if ontology_id:
                yield ontology_id

    def ontology_metadata_map(self, ontology: CURIE) -> Dict[PRED_CURIE, List[str]]:
        metadata = self.client.get_ontology(ontology)
        config = (metadata or {}).get("config") or {}
        metadata_map: Dict[PRED_CURIE, List[str]] = {}
        for key, predicate in [
            ("title", "dcterms:title"),
            ("description", "dcterms:description"),
            ("version", "owl:versionInfo"),
            ("versionIri", "owl:versionIRI"),
            ("fileLocation", "schema:url"),
            ("homepage", "foaf:homepage"),
        ]:
            value = config.get(key)
            if value:
                metadata_map[predicate] = [value]
        return metadata_map

    def ontology_versions(self, ontology: CURIE) -> Iterable[str]:
        metadata = self.client.get_ontology(ontology)
        version = ((metadata or {}).get("config") or {}).get("version")
        if version:
            yield version

    def languages(self) -> Iterable[LANGUAGE_TAG]:
        """Yield the language tags OLS holds translations for in the focus ontology."""
        if not self.focus_ontology:
            return
        metadata = self.client.get_ontology(self.focus_ontology) or {}
        yield from metadata.get("languages") or []

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: OboGraphInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> Optional[obograph.Node]:
        """
        Build an OBO Graph node from the OLS term payload.

        :param curie: entity to look up
        :param strict: raise a ValueError if OLS has no such term
        :param include_metadata: include the term's metadata block
        :param expand_curies: use full URIs rather than CURIEs for the node id
        :return: an obograph Node
        """
        term = self.term_metadata(curie)
        node_id = curie
        if expand_curies:
            node_id = self.curie_to_uri(curie) or curie
        if term is None:
            if strict:
                raise ValueError(f"Unknown entity: {curie}")
            return obograph.Node(id=node_id)
        meta = obograph.Meta()
        definition = _scalar(term.get("description"))
        if definition:
            meta.definition = obograph.DefinitionPropertyValue(val=definition)
            xrefs = self._definition_xrefs(curie)
            if xrefs:
                meta.definition.xrefs = xrefs
        for xref in term.get("obo_xref") or []:
            curie_xref = _xref_curie(xref)
            if curie_xref is not None:
                meta.xrefs.append(obograph.XrefPropertyValue(val=curie_xref))
        for subset in term.get("in_subset") or []:
            meta.subsets.append(subset)
        if term.get("is_obsolete"):
            meta.deprecated = True
        for _, synonym in self.synonym_property_values([curie]):
            meta.synonyms.append(synonym)
        if include_metadata:
            handled = {HAS_DEFINITION_CURIE, HAS_DBXREF, IN_SUBSET, "rdfs:label"}
            for predicate, values in self.entity_metadata_map(curie).items():
                if predicate in handled or predicate in SCOPE_TO_SYNONYM_PRED_MAP.values():
                    continue
                for value in values:
                    meta.basicPropertyValues.append(
                        obograph.BasicPropertyValue(pred=predicate, val=value)
                    )
        return obograph.Node(id=node_id, lbl=_scalar(term.get("label")), type="CLASS", meta=meta)

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

    def relationships(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
        invert: bool = False,
    ) -> Iterator[RELATIONSHIP]:
        """
        Yield relationships from OLS term graph and hierarchy endpoints.

        Direct relationships are read from the OLS ``graph`` endpoint. Entailed
        hierarchy relationships are read from OLS closure endpoints:
        ``ancestors``/``descendants`` for ``is_a`` and, when the ontology has no
        other configured hierarchy predicates, the extra nodes from
        ``hierarchicalAncestors``/``hierarchicalDescendants`` for ``part_of``.

        :param subjects: constrain search to these subjects
        :param predicates: constrain search to these predicates
        :param objects: constrain search to these objects
        :param include_tbox: accepted for interface compatibility
        :param include_abox: accepted for interface compatibility
        :param include_entailed: include hierarchy closure edges
        :param exclude_blank: accepted for interface compatibility
        :param invert: invert subject/object constraints and returned triples
        :return: relationship triples
        """
        if invert:
            for s, p, o in self.relationships(
                subjects=objects,
                predicates=predicates,
                objects=subjects,
                include_tbox=include_tbox,
                include_abox=include_abox,
                include_entailed=include_entailed,
                exclude_blank=exclude_blank,
            ):
                yield o, p, s
            return

        subject_list = list(subjects) if subjects else None
        object_list = list(objects) if objects else None
        predicate_list = list(predicates) if predicates else None

        if not subject_list and not object_list:
            raise NotImplementedError(
                "OLS relationships must be constrained by subjects or objects"
            )

        if include_entailed:
            yield from self._entailed_hierarchy_relationships(
                subjects=subject_list,
                predicates=predicate_list,
                objects=object_list,
            )
            return

        yielded = set()
        if subject_list:
            object_set = set(object_list) if object_list else None
            for subject in subject_list:
                for rel in self._graph_relationships(
                    subject,
                    predicates=predicate_list,
                    subjects={subject},
                    objects=object_set,
                ):
                    if rel not in yielded:
                        yielded.add(rel)
                        yield rel
        else:
            for obj in object_list:
                for rel in self._graph_relationships(
                    obj,
                    predicates=predicate_list,
                    objects={obj},
                ):
                    if rel not in yielded:
                        yielded.add(rel)
                        yield rel

    def _graph_relationships(
        self,
        focus_curie: CURIE,
        predicates: List[PRED_CURIE] = None,
        subjects: set = None,
        objects: set = None,
    ) -> Iterator[RELATIONSHIP]:
        """Return direct graph relationships from the OLS term graph endpoint."""
        ontology = self.focus_ontology
        iri = self.curie_to_uri(focus_curie)
        path = f"ontologies/{ontology}/terms/{_double_quote_iri(iri)}/graph"
        response = self.client.get_json(path)
        for edge in (response or {}).get("edges") or []:
            if not isinstance(edge, dict):
                continue
            source = edge.get("source")
            predicate = edge.get("uri")
            target = edge.get("target")
            if not all(isinstance(value, str) and value for value in (source, predicate, target)):
                continue
            subject_curie = self.uri_to_curie(source, strict=False, use_uri_fallback=True)
            predicate_curie = self.uri_to_curie(predicate, strict=False, use_uri_fallback=True)
            object_curie = self.uri_to_curie(target, strict=False, use_uri_fallback=True)
            relationship = (subject_curie, predicate_curie, object_curie)
            if not all(isinstance(value, str) and value for value in relationship):
                continue
            if subjects and subject_curie not in subjects:
                continue
            if objects and object_curie not in objects:
                continue
            if predicates and predicate_curie not in predicates:
                continue
            yield relationship

    def _entailed_hierarchy_relationships(
        self,
        subjects: List[CURIE] = None,
        predicates: List[PRED_CURIE] = None,
        objects: List[CURIE] = None,
    ) -> Iterator[RELATIONSHIP]:
        """Return entailed hierarchy relationships supported by OLS closures."""
        supported_predicates = {IS_A, PART_OF}
        predicate_set = set(predicates) if predicates else supported_predicates
        unsupported_predicates = predicate_set - supported_predicates
        if unsupported_predicates:
            raise NotImplementedError(
                "OLS entailed relationships support only "
                f"{sorted(supported_predicates)}; got {sorted(predicate_set)}"
            )
        if PART_OF in predicate_set:
            additional_hierarchical_predicates = (
                self._ols_hierarchical_predicates() - supported_predicates
            )
            if additional_hierarchical_predicates:
                raise NotImplementedError(
                    "OLS cannot distinguish entailed part_of relationships from "
                    "the ontology's additional hierarchical predicates: "
                    f"{sorted(additional_hierarchical_predicates)}"
                )

        yielded = set()
        if subjects:
            object_set = set(objects) if objects else None
            for subject in subjects:
                for rel in self._entailed_hierarchy_relationships_from_subject(
                    subject, predicate_set, object_set
                ):
                    if rel not in yielded:
                        yielded.add(rel)
                        yield rel
        elif objects:
            for obj in objects:
                for rel in self._entailed_hierarchy_relationships_to_object(obj, predicate_set):
                    if rel not in yielded:
                        yielded.add(rel)
                        yield rel

    def _entailed_hierarchy_relationships_from_subject(
        self, subject: CURIE, predicate_set: set, objects: set = None
    ) -> Iterator[RELATIONSHIP]:
        isa_ancestors = set(self.ancestors(subject, predicates=[IS_A], reflexive=True))
        if IS_A in predicate_set:
            for obj in isa_ancestors:
                if objects and obj not in objects:
                    continue
                yield subject, IS_A, obj
        if PART_OF in predicate_set:
            hierarchy_ancestors = set(
                self.ancestors(subject, predicates=[IS_A, PART_OF], reflexive=True)
            )
            for obj in hierarchy_ancestors - isa_ancestors:
                if objects and obj not in objects:
                    continue
                yield subject, PART_OF, obj

    def _ols_hierarchical_predicates(self) -> set[PRED_CURIE]:
        """Return the predicates included in the OLS hierarchical closure.

        OLS always includes ``rdfs:subClassOf``. Its ontology metadata reports
        additional predicates in ``config.hierarchicalProperties``; when that
        setting is empty or absent, OLS defaults to ``part_of``.
        """
        metadata = self.client.get_ontology(self.focus_ontology)
        config = metadata.get("config") if isinstance(metadata, dict) else None
        if not isinstance(config, dict):
            raise NotImplementedError(
                "OLS ontology metadata does not expose configured hierarchical predicates"
            )
        configured_properties = config.get("hierarchicalProperties") or [self.curie_to_uri(PART_OF)]
        if isinstance(configured_properties, str):
            configured_properties = [configured_properties]

        predicates = {IS_A}
        for property_iri in configured_properties:
            predicate = self.uri_to_curie(property_iri, strict=False, use_uri_fallback=True)
            if predicate:
                predicates.add(predicate)
        return predicates

    def _entailed_hierarchy_relationships_to_object(
        self, obj: CURIE, predicate_set: set
    ) -> Iterator[RELATIONSHIP]:
        isa_descendants = set(self.descendants(obj, predicates=[IS_A], reflexive=True))
        if IS_A in predicate_set:
            for subject in isa_descendants:
                yield subject, IS_A, obj
        if PART_OF in predicate_set:
            hierarchy_descendants = set(
                self.descendants(obj, predicates=[IS_A, PART_OF], reflexive=True)
            )
            for subject in hierarchy_descendants - isa_descendants:
                yield subject, PART_OF, obj

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
            iri = record.get("iri")
            if not iri:
                continue
            # OLS indexes ontologies whose IRIs have no registered prefix; keep the
            # IRI rather than yielding None for those
            curie = self.uri_to_curie(iri, strict=False, use_uri_fallback=True)
            if not curie:
                continue
            self.label_cache[curie] = record.get("label")
            yield curie

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingsInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        """Yield the cross-references OLS holds for a term."""
        term = self.term_metadata(curie) or {}
        for xref in term.get("obo_xref") or []:
            curie_xref = _xref_curie(xref)
            if curie_xref is not None:
                yield HAS_DBXREF, curie_xref

    def get_sssom_mappings_by_curie(self, curie: Union[str, CURIE]) -> Iterator[Mapping]:
        """
        Yield SSSOM mappings for a term.

        Mappings come from two sources: the cross-references OLS itself records for the
        term, and the (separate) OxO mapping service.
        """
        seen = set()
        for predicate_id, object_id in self.simple_mappings_by_curie(curie):
            key = (curie, predicate_id, object_id)
            if key in seen:
                continue
            seen.add(key)
            mapping = Mapping(
                subject_id=curie,
                subject_label=self.label(curie),
                predicate_id=predicate_id,
                object_id=object_id,
                mapping_justification=SEMAPV.UnspecifiedMatching.value,
            )
            inject_mapping_sources(mapping)
            yield mapping
        yield from self.oxo_mappings_by_curie(curie)

    def oxo_mappings_by_curie(self, curie: Union[str, CURIE]) -> Iterator[Mapping]:
        """Yield mappings for a term from the EBI OxO service."""
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
