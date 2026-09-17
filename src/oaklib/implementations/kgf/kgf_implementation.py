"""Adapter for KGF (Knowledge Graph Framework) services such as `<https://apps.okn.us/kgf>`_."""

import logging
from collections import OrderedDict, defaultdict
from copy import copy
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

import requests
from sssom_schema import Mapping

from oaklib.constants import TIMEOUT_SECONDS
from oaklib.datamodels import obograph
from oaklib.datamodels.search import (
    DEFAULT_SEARCH_PROPERTIES,
    SearchConfiguration,
    SearchProperty,
)
from oaklib.datamodels.search_datamodel import SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    ALL_MATCH_PREDICATES,
    BIOLINK_CATEGORY,
    DEPRECATED_PREDICATE,
    HAS_DBXREF,
    HAS_DEFINITION_CURIE,
    IN_SUBSET,
    LABEL_PREDICATE,
    OWL_ANNOTATION_PROPERTY,
    OWL_CLASS,
    OWL_DATATYPE_PROPERTY,
    OWL_NAMED_INDIVIDUAL,
    OWL_OBJECT_PROPERTY,
    RDF_TYPE,
    RDFS_COMMENT,
    SKOS_DEFINITION_CURIE,
    STANDARD_ANNOTATION_PROPERTIES,
    SYNONYM_PREDICATES,
    TERM_REPLACED_BY,
)
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    METADATA_MAP,
    PREFIX_MAP,
    RELATIONSHIP,
    get_default_prefix_map,
)
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.interfaces.search_interface import SearchInterface
from oaklib.types import CURIE, LANGUAGE_TAG, PRED_CURIE, URI

__all__ = [
    "DEFAULT_KGF_BASE_URL",
    "KGFImplementation",
]

logger = logging.getLogger(__name__)

#: The public FRINK/Proto-OKN deployment of KGF.
DEFAULT_KGF_BASE_URL = "https://apps.okn.us/kgf"

#: KGF skolemizes blank nodes as IRIs in a ``urn:fdc:`` namespace containing this marker.
BNODE_MARKER = ":kgf:bnode:"

#: Predicates consulted, in order, when looking up a textual definition.
DEFINITION_PREDICATES = [
    HAS_DEFINITION_CURIE,
    SKOS_DEFINITION_CURIE,
    "dcterms:description",
    "schema:description",
]

#: ``rdf:type`` values enumerated by :meth:`KGFImplementation.entities`.
DEFAULT_OWL_TYPES = [
    OWL_CLASS,
    OWL_OBJECT_PROPERTY,
    OWL_ANNOTATION_PROPERTY,
    OWL_DATATYPE_PROPERTY,
    OWL_NAMED_INDIVIDUAL,
]

#: IRI-valued predicates that :meth:`KGFImplementation.entity_metadata_map` reports as metadata.
IRI_VALUED_ANNOTATION_PREDICATES = set(
    STANDARD_ANNOTATION_PROPERTIES
    + ALL_MATCH_PREDICATES
    + [IN_SUBSET, RDF_TYPE, TERM_REPLACED_BY, BIOLINK_CATEGORY, "rdfs:isDefinedBy"]
)

#: Maps OAK synonym predicates onto the obograph ``ScopeEnum`` values.
SYNONYM_PRED_TO_SCOPE = {
    "oio:hasExactSynonym": "hasExactSynonym",
    "oio:hasNarrowSynonym": "hasNarrowSynonym",
    "oio:hasBroadSynonym": "hasBroadSynonym",
    "oio:hasRelatedSynonym": "hasRelatedSynonym",
}

XSD_BOOLEAN = "http://www.w3.org/2001/XMLSchema#boolean"

#: KGF operations that answer in a single page: they take no ``cursor``.
_UNPAGED_OPS = {"search", "sample"}

#: Rows key used by each KGF operation that returns a collection.
_ROWS_KEY = {
    "fragment": "rows",
    "describe": "rows",
    "sample": "rows",
    "terms": "terms",
    "search": "results",
    "labels": "labels",
}


def _escape_literal(value: str) -> str:
    """Escape a lexical form for KGF's N-Triples-style term syntax."""
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


def _literal_term(value: str, lang: Optional[str] = None, datatype: Optional[URI] = None) -> str:
    """Render a literal in the term syntax KGF accepts for the ``s``/``p``/``o`` parameters."""
    term = f'"{_escape_literal(value)}"'
    if lang:
        return f"{term}@{lang}"
    if datatype:
        return f"{term}^^<{datatype}>"
    return term


def _enum_name(value: Any) -> Optional[str]:
    """The permissible-value text of a LinkML enum value, however it was supplied."""
    if value is None:
        return None
    return value.text if hasattr(value, "text") else str(value)


def _is_blank(node: Dict[str, Any]) -> bool:
    """True if a KGF term object stands for a blank node (including skolemized ones)."""
    if node.get("type") == "bnode":
        return True
    return node.get("type") == "iri" and BNODE_MARKER in node.get("value", "")


@dataclass
class KGFImplementation(OboGraphInterface, MappingProviderInterface, SearchInterface):
    """
    An adapter for datasets served by a KGF (Knowledge Graph Framework) endpoint.

    KGF serves immutable, versioned RDF bundles over a small read-only HTTP API
    (triple pattern fragments, node description, full-text search, batch label lookup).
    The reference deployment is the FRINK / Proto-OKN service at
    `<https://apps.okn.us/kgf>`_, which hosts several dozen knowledge graphs
    including Ubergraph.

    The selector is ``kgf:`` followed by a dataset identifier, as listed by
    ``GET https://apps.okn.us/kgf``:

    >>> from oaklib import get_adapter
    >>> adapter = get_adapter("kgf:ubergraph")  # doctest: +SKIP
    >>> adapter.label("GO:0005634")  # doctest: +SKIP
    'nucleus'

    Bundles are versioned, and by default the release the service marks as ``current``
    is used. A specific release can be pinned with ``@``:

    >>> adapter = get_adapter("kgf:ubergraph@v0.0.2")  # doctest: +SKIP

    To reach a dataset on a different KGF deployment, give its full URL:

    >>> adapter = get_adapter("kgf:https://apps.okn.us/kgf/sockg")  # doctest: +SKIP

    .. note ::

        KGF exposes triple patterns rather than a query language, so operations that
        would be a single SPARQL query elsewhere become one or more HTTP requests here.
        Whole-graph operations such as :meth:`entities` page through the service and can
        be slow on the larger bundles.
    """

    base_url: str = DEFAULT_KGF_BASE_URL
    """Root of the KGF deployment; only used when the selector names a bare dataset."""

    dataset: Optional[str] = None
    """Identifier of the dataset (bundle) within the deployment, e.g. ``ubergraph``."""

    version: Optional[str] = None
    """Release of the dataset, e.g. ``v0.0.2``. Defaults to the release marked ``current``."""

    page_size: int = 1000
    """Number of rows requested per page when paging through a triple pattern."""

    node_cache_size: int = 500
    """How many node descriptions to keep in memory."""

    starts_with_scan_limit: int = 200
    """How many distinct literals a starts-with search may scan; see :meth:`basic_search`."""

    _dataset_url: Optional[str] = None
    _manifest: Optional[Dict[str, Any]] = None
    _dataset_info: Optional[Dict[str, Any]] = None
    _caps: Optional[Dict[str, Any]] = None
    _session: Optional[requests.Session] = None
    _node_cache: "OrderedDict[CURIE, List[Tuple[PRED_CURIE, Dict[str, Any]]]]" = field(
        default_factory=OrderedDict
    )
    _obsoletes: Optional[List[CURIE]] = None

    def __post_init__(self):
        slug = self.resource.slug if self.resource else None
        if slug:
            slug, _, version = slug.partition("@")
            if version and not self.version:
                self.version = version
            if slug.startswith("http://") or slug.startswith("https://"):
                self._dataset_url = slug.rstrip("/")
                self.dataset = self._dataset_url.rsplit("/", 1)[-1]
            else:
                self.dataset = slug
        if not self.dataset:
            raise ValueError(
                "A KGF dataset must be named, e.g. 'kgf:ubergraph'. "
                f"Datasets available on a deployment are listed by GET {self.base_url}"
            )
        if not self._dataset_url:
            self._dataset_url = f"{self.base_url.rstrip('/')}/{self.dataset}"

    # ------------------------------------------------------------------
    # HTTP plumbing
    # ------------------------------------------------------------------

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
        return self._session

    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        logger.debug(f"KGF {method} {url} {kwargs.get('params') or kwargs.get('json')}")
        response = self.session.request(method, url, timeout=TIMEOUT_SECONDS, **kwargs)
        if not response.ok:
            detail = response.text
            try:
                # KGF reports errors as RFC 7807 problem documents
                detail = response.json().get("detail", detail)
            except ValueError:
                pass
            raise ValueError(f"KGF request failed ({response.status_code}) for {url}: {detail}")
        return response.json()

    def dataset_info(self) -> Dict[str, Any]:
        """Metadata for the dataset, including the list of available releases."""
        if self._dataset_info is None:
            self._dataset_info = self._request("GET", self._dataset_url)
        return self._dataset_info

    def current_version(self) -> str:
        """The release of the dataset this adapter is bound to."""
        if not self.version:
            info = self.dataset_info()
            version = info.get("current")
            if not version:
                raise ValueError(f"KGF dataset {self.dataset} publishes no current release")
            self.version = version
        return self.version

    @property
    def endpoint_url(self) -> str:
        """Base URL of the release, under which the KGF operations are served."""
        return f"{self._dataset_url}/v/{self.current_version()}"

    def manifest(self) -> Dict[str, Any]:
        """The bundle manifest: counts, prefixes, capabilities, provenance."""
        if self._manifest is None:
            self._manifest = self._request("GET", f"{self.endpoint_url}/manifest")
        return self._manifest

    def caps(self) -> Dict[str, Any]:
        """Per-request limits published by the deployment."""
        if self._caps is None:
            try:
                self._caps = self._request("GET", self.base_url.rstrip("/")).get("caps", {})
            except ValueError:
                logger.warning(f"Could not read caps from {self.base_url}; assuming defaults")
                self._caps = {}
        return self._caps

    def _op(self, op: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("GET", f"{self.endpoint_url}/{op}", params=params)

    def _paged(
        self,
        op: str,
        params: Dict[str, Any],
        limit: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Iterator[Any]:
        """Yield rows from a KGF operation, following its cursor until exhausted.

        Operations in :data:`_UNPAGED_OPS` answer in a single page and reject a cursor,
        so for those this yields at most one page.

        :param op: operation name, e.g. ``fragment``
        :param params: query parameters; ``limit`` and ``cursor`` are managed here
        :param limit: stop after this many rows
        :param page_size: rows per request, where the operation's cap is below the default
        """
        key = _ROWS_KEY[op]
        params = {k: v for k, v in params.items() if v is not None}
        max_page = min(page_size, self.page_size) if page_size else self.page_size
        n = 0
        while True:
            this_page = max_page
            if limit is not None:
                this_page = min(this_page, limit - n)
                if this_page <= 0:
                    return
            body = self._op(op, {**params, "limit": this_page})
            for row in body.get(key) or []:
                yield row
                n += 1
                if limit is not None and n >= limit:
                    return
            cursor = body.get("next")
            if not cursor or op in _UNPAGED_OPS:
                return
            params = {**params, "cursor": cursor}

    # ------------------------------------------------------------------
    # Term (de)serialization
    # ------------------------------------------------------------------

    def prefix_map(self) -> PREFIX_MAP:
        """OAK's default prefix map, extended with any prefixes the bundle declares."""
        if not self._prefix_map:
            prefix_map = copy(get_default_prefix_map())
            for prefix, expansion in (self.manifest().get("prefixes") or {}).items():
                prefix_map.setdefault(prefix, expansion)
            self._prefix_map = prefix_map
        return self._prefix_map

    def _uri(self, curie: CURIE) -> Optional[URI]:
        """Expand a CURIE to an IRI, passing IRIs through unchanged."""
        if curie.startswith("http://") or curie.startswith("https://") or curie.startswith("urn:"):
            return curie
        uri = self.converter.expand(curie)
        if uri is None:
            # routine rather than exceptional: OBO xrefs, for one, name prefixes that
            # neither OAK nor the bundle declares
            logger.info(f"Cannot expand {curie} using the prefixes known to {self.dataset}")
        return uri

    def _term(self, curie: CURIE) -> Optional[str]:
        """Render a CURIE or IRI as a bracketed IRI term for the KGF query parameters."""
        uri = self._uri(curie)
        return f"<{uri}>" if uri else None

    def _terms(self, curies: Optional[Iterable[CURIE]]) -> Optional[str]:
        """Render several CURIEs as the comma-separated list KGF's ``predicate`` takes."""
        if not curies:
            return None
        terms = [t for t in (self._term(c) for c in curies) if t]
        return ",".join(terms) if terms else None

    def _curie(self, node: Dict[str, Any]) -> Optional[CURIE]:
        """Compress a KGF IRI term to a CURIE; returns None for literals."""
        if node.get("type") != "iri":
            return None
        uri = node["value"]
        return self.converter.compress(uri) or uri

    def _normalize(self, curie: CURIE) -> CURIE:
        """Put an identifier into the CURIE form this adapter yields, if there is one."""
        uri = self._uri(curie)
        return (self.converter.compress(uri) or uri) if uri else curie

    @staticmethod
    def _value(node: Dict[str, Any]) -> Any:
        """The Python value of a KGF term object."""
        return node.get("value")

    # ------------------------------------------------------------------
    # Node descriptions
    # ------------------------------------------------------------------

    def _outgoing_statements(self, curie: CURIE) -> List[Tuple[PRED_CURIE, Dict[str, Any]]]:
        """All statements with ``curie`` as subject, as (predicate, object-term) pairs.

        A whole node is fetched in one ``describe`` call and cached, because ``label``,
        ``definition``, ``entity_alias_map`` and friends are typically called in sequence
        on the same entity.
        """
        if curie in self._node_cache:
            self._node_cache.move_to_end(curie)
            return self._node_cache[curie]
        term = self._term(curie)
        statements: List[Tuple[PRED_CURIE, Dict[str, Any]]] = []
        if term:
            for row in self._paged("describe", {"iri": term, "direction": "out"}):
                predicate = self._curie(row["p"])
                if predicate:
                    statements.append((predicate, row["o"]))
        self._node_cache[curie] = statements
        self._node_cache.move_to_end(curie)
        while len(self._node_cache) > self.node_cache_size:
            self._node_cache.popitem(last=False)
        return statements

    def _values(self, curie: CURIE, predicates: Iterable[PRED_CURIE]) -> Iterator[Dict[str, Any]]:
        predicates = set(predicates)
        for predicate, node in self._outgoing_statements(curie):
            if predicate in predicates:
                yield node

    # ------------------------------------------------------------------
    # BasicOntologyInterface
    # ------------------------------------------------------------------

    def ontologies(self) -> Iterable[CURIE]:
        yield self.dataset

    def ontology_versions(self, ontology: CURIE) -> Iterable[str]:
        for release in self.dataset_info().get("releases") or []:
            if "version" in release:
                yield release["version"]

    def ontology_metadata_map(self, ontology: CURIE) -> METADATA_MAP:
        manifest = self.manifest()
        metadata: METADATA_MAP = {"id": [manifest.get("dataset_iri") or self.dataset]}
        for key in ("title", "description", "homepage", "version", "created", "content_digest"):
            if manifest.get(key):
                metadata[key] = [manifest[key]]
        publisher = manifest.get("publisher") or {}
        if publisher.get("name"):
            metadata["publisher"] = [publisher["name"]]
        for key, value in (manifest.get("counts") or {}).items():
            metadata[f"count_{key}"] = [value]
        return metadata

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        owl_types = [owl_type] if owl_type else DEFAULT_OWL_TYPES
        obsoletes = set(self.obsoletes()) if filter_obsoletes else set()
        seen = set()
        for t in owl_types:
            type_term = self._term(t)
            if not type_term:
                continue
            for row in self._paged("fragment", {"p": self._term(RDF_TYPE), "o": type_term}):
                node = row["s"]
                if _is_blank(node):
                    continue
                curie = self._curie(node)
                if curie is None or curie in seen or curie in obsoletes:
                    continue
                seen.add(curie)
                yield curie

    def obsoletes(self, include_merged=True) -> Iterable[CURIE]:
        if self._obsoletes is None:
            obsoletes = []
            for row in self._paged(
                "fragment",
                {
                    "p": self._term(DEPRECATED_PREDICATE),
                    "o": _literal_term("true", datatype=XSD_BOOLEAN),
                },
            ):
                node = row["s"]
                if _is_blank(node):
                    continue
                curie = self._curie(node)
                if curie:
                    obsoletes.append(curie)
            self._obsoletes = obsoletes
        yield from self._obsoletes

    def owl_types(self, entities: Iterable[CURIE]) -> Iterable[Tuple[CURIE, CURIE]]:
        for curie in entities:
            for node in self._values(curie, [RDF_TYPE]):
                type_curie = self._curie(node)
                if type_curie:
                    yield curie, type_curie

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        for _, label in self.labels([curie], lang=lang):
            return label
        return None

    def labels(
        self, curies: Iterable[CURIE], allow_none=True, lang: LANGUAGE_TAG = None
    ) -> Iterable[Tuple[CURIE, str]]:
        if lang:
            # the batch endpoint returns one label per IRI with no language tag,
            # so language-specific lookups go through the node description instead
            for curie in curies:
                label = None
                for node in self._values(curie, self._label_predicates()):
                    if node.get("lang") == lang:
                        label = self._value(node)
                        break
                if label is not None or allow_none:
                    yield curie, label
            return
        batch_size = min(self.caps().get("max_label_iris", 1000), 1000)
        batch: List[CURIE] = []
        for curie in curies:
            batch.append(curie)
            if len(batch) >= batch_size:
                yield from self._labels_batch(batch, allow_none)
                batch = []
        if batch:
            yield from self._labels_batch(batch, allow_none)

    def _labels_batch(
        self, curies: List[CURIE], allow_none: bool
    ) -> Iterator[Tuple[CURIE, Optional[str]]]:
        by_uri = {}
        for curie in curies:
            uri = self._uri(curie)
            if uri:
                by_uri[uri] = curie
        labels: Dict[CURIE, Optional[str]] = {}
        if by_uri:
            body = self._request(
                "POST",
                f"{self.endpoint_url}/labels",
                json={"iris": [f"<{uri}>" for uri in by_uri]},
            )
            for row in body.get("labels") or []:
                curie = by_uri.get(row["iri"]["value"])
                if curie is not None:
                    labels[curie] = row.get("label")
        for curie in curies:
            label = labels.get(curie)
            if label is None and not allow_none:
                continue
            yield curie, label

    def _label_predicates(self) -> List[PRED_CURIE]:
        """Predicates the bundle declares as playing the ``label`` role."""
        roles = (self.manifest().get("predicate_roles") or {}).get("label") or []
        predicates = [self.converter.compress(uri) or uri for uri in roles]
        return predicates or [LABEL_PREDICATE]

    def curies_by_label(self, label: str) -> List[CURIE]:
        curies = []
        for predicate in self._label_predicates():
            predicate_term = self._term(predicate)
            if not predicate_term:
                continue
            for row in self._paged("fragment", {"p": predicate_term, "o": _literal_term(label)}):
                curie = self._curie(row["s"])
                if curie and curie not in curies:
                    curies.append(curie)
        return curies

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        for predicate in DEFINITION_PREDICATES:
            for node in self._values(curie, [predicate]):
                if lang and node.get("lang") != lang:
                    continue
                return self._value(node)
        return None

    def comments(
        self, curies: Iterable[CURIE], allow_none=True
    ) -> Iterator[Tuple[CURIE, Optional[str]]]:
        for curie in curies:
            comment = None
            for node in self._values(curie, [RDFS_COMMENT]):
                comment = self._value(node)
                break
            if comment is None and not allow_none:
                continue
            yield curie, comment

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        alias_map: ALIAS_MAP = defaultdict(list)
        alias_predicates = set(SYNONYM_PREDICATES) | {LABEL_PREDICATE}
        for predicate, node in self._outgoing_statements(curie):
            if predicate in alias_predicates and node.get("type") == "literal":
                alias_map[predicate].append(self._value(node))
        return dict(alias_map)

    def entity_metadata_map(self, curie: CURIE, include_all_triples=False) -> METADATA_MAP:
        metadata: METADATA_MAP = defaultdict(list)
        metadata["id"] = [curie]
        for predicate, node in self._outgoing_statements(curie):
            if node.get("type") == "literal":
                metadata[predicate].append(self._value(node))
            elif include_all_triples or predicate in IRI_VALUED_ANNOTATION_PREDICATES:
                if _is_blank(node):
                    continue
                value = self._curie(node)
                if value:
                    metadata[predicate].append(value)
        return dict(metadata)

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        for predicate, node in self._outgoing_statements(curie):
            if predicate not in ALL_MATCH_PREDICATES:
                continue
            if node.get("type") == "literal":
                # OBO-style xrefs are literals holding a CURIE
                yield predicate, self._value(node)
            elif not _is_blank(node):
                object_curie = self._curie(node)
                if object_curie:
                    yield predicate, object_curie

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
        """Yield entity-to-entity statements matching the pattern.

        Statements whose object is a literal are not relationships and are never
        yielded; see :meth:`entity_metadata_map` for those.

        A KGF bundle is served exactly as it was built, with no reasoning layer on top,
        so ``include_tbox``, ``include_abox`` and ``include_entailed`` have no effect:
        whether entailed edges are present is a property of the bundle. The Ubergraph
        bundle, for instance, materializes its inferred ``rdfs:subClassOf`` edges.
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
        subjects = list(subjects) if subjects is not None else None
        predicates = list(predicates) if predicates is not None else None
        objects = list(objects) if objects is not None else None
        if subjects is not None and predicates is None and objects is None:
            # one cached describe per subject beats one fragment call per predicate
            for subject in subjects:
                for predicate, node in self._outgoing_statements(subject):
                    if node.get("type") != "iri":
                        continue
                    if exclude_blank and _is_blank(node):
                        continue
                    object_curie = self._curie(node)
                    if object_curie:
                        yield subject, predicate, object_curie
            return
        for subject in subjects or [None]:
            for predicate in predicates or [None]:
                for object_ in objects or [None]:
                    yield from self._relationships_for_pattern(
                        subject, predicate, object_, exclude_blank
                    )

    def _relationships_for_pattern(
        self,
        subject: Optional[CURIE],
        predicate: Optional[PRED_CURIE],
        object_: Optional[CURIE],
        exclude_blank: bool,
    ) -> Iterator[RELATIONSHIP]:
        params = {}
        for key, value in (("s", subject), ("p", predicate), ("o", object_)):
            if value is None:
                continue
            term = self._term(value)
            if term is None:
                return
            params[key] = term
        # bound positions come back from the query rather than the response, so put them
        # in the same CURIE form the unbound positions will be in
        subject = self._normalize(subject) if subject else None
        predicate = self._normalize(predicate) if predicate else None
        object_ = self._normalize(object_) if object_ else None
        for row in self._paged("fragment", params):
            # KGF omits bound positions from the rows, so fill them back in
            subject_node = row.get("s")
            object_node = row.get("o")
            predicate_node = row.get("p")
            if object_node is not None and object_node.get("type") != "iri":
                continue
            if exclude_blank and (
                (subject_node is not None and _is_blank(subject_node))
                or (object_node is not None and _is_blank(object_node))
            ):
                continue
            s = subject if subject_node is None else self._curie(subject_node)
            p = predicate if predicate_node is None else self._curie(predicate_node)
            o = object_ if object_node is None else self._curie(object_node)
            if s and p and o:
                yield s, p, o

    # ------------------------------------------------------------------
    # OboGraphInterface
    # ------------------------------------------------------------------

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> Optional[obograph.Node]:
        statements = self._outgoing_statements(curie)
        if not statements:
            if strict:
                raise ValueError(f"No such node: {curie} in {self.dataset}")
            return None
        node = obograph.Node(id=self.curie_to_uri(curie) if expand_curies else curie)
        meta = obograph.Meta()
        basic_property_values = []
        for predicate, value_node in statements:
            literal = value_node.get("type") == "literal"
            value = self._value(value_node) if literal else self._curie(value_node)
            if value is None:
                continue
            if predicate == LABEL_PREDICATE and literal:
                node.lbl = value
            elif predicate == RDF_TYPE:
                if value == OWL_CLASS:
                    node.type = "CLASS"
                elif value == OWL_NAMED_INDIVIDUAL:
                    node.type = "INDIVIDUAL"
                elif value in (OWL_OBJECT_PROPERTY, OWL_ANNOTATION_PROPERTY, OWL_DATATYPE_PROPERTY):
                    node.type = "PROPERTY"
            elif predicate in DEFINITION_PREDICATES and literal and not meta.definition:
                meta.definition = obograph.DefinitionPropertyValue(val=value)
            elif predicate in SYNONYM_PREDICATES and literal:
                meta.synonyms.append(
                    obograph.SynonymPropertyValue(
                        pred=SYNONYM_PRED_TO_SCOPE.get(predicate, "hasRelatedSynonym"),
                        val=value,
                    )
                )
            elif predicate == HAS_DBXREF:
                meta.xrefs.append(obograph.XrefPropertyValue(val=value))
            elif predicate == IN_SUBSET:
                meta.subsets.append(value)
            elif predicate == DEPRECATED_PREDICATE:
                meta.deprecated = str(value).lower() == "true"
            elif include_metadata and not _is_blank(value_node):
                if literal or predicate in IRI_VALUED_ANNOTATION_PREDICATES:
                    basic_property_values.append(
                        obograph.BasicPropertyValue(pred=predicate, val=value)
                    )
        if include_metadata:
            meta.basicPropertyValues = basic_property_values
        node.meta = meta
        return node

    # ------------------------------------------------------------------
    # MappingProviderInterface
    # ------------------------------------------------------------------

    def get_sssom_mappings_by_curie(self, curie: Union[CURIE, URI]) -> Iterator[Mapping]:
        for predicate, object_id in self.simple_mappings_by_curie(curie):
            yield Mapping(
                subject_id=curie,
                predicate_id=predicate,
                object_id=object_id,
                mapping_justification="semapv:UnspecifiedMatching",
            )

    # ------------------------------------------------------------------
    # SearchInterface
    # ------------------------------------------------------------------

    def basic_search(
        self, search_term: str, config: Optional[SearchConfiguration] = None
    ) -> Iterable[CURIE]:
        """Search the bundle's full-text index over label and synonym literals.

        KGF's index is token-based: it has no substring, wildcard or regular expression
        matching. Exact and partial searches are answered by the index and then filtered
        locally; ``STARTS_WITH`` searches use KGF's ordered term scan instead, which is
        case-sensitive. Regular expression and SQL search syntaxes are not supported.
        """
        if config is None:
            config = SearchConfiguration()
        syntax = _enum_name(config.syntax)
        if syntax in (SearchTermSyntax.REGULAR_EXPRESSION.text, SearchTermSyntax.SQL.text):
            raise NotImplementedError(
                f"KGF has no {syntax} search; use exact, partial or starts-with search"
            )
        limit = config.limit
        predicates = self._search_predicates(config)
        if syntax == SearchTermSyntax.STARTS_WITH.text:
            yield from self._starts_with_search(search_term, predicates, limit)
            return
        max_results = min(self.caps().get("max_search_results", 1000), 1000)
        params = {"q": search_term, "predicate": self._terms(predicates), "labels": "false"}
        seen = set()
        n = 0
        for result in self._paged("search", params, limit=max_results, page_size=max_results):
            if not config.is_partial:
                literal = (result.get("match") or {}).get("literal") or ""
                if literal.casefold() != search_term.casefold():
                    continue
            subject = result["subject"]
            if _is_blank(subject):
                continue
            curie = self._curie(subject)
            if curie is None or curie in seen:
                continue
            seen.add(curie)
            yield curie
            n += 1
            if limit is not None and n >= limit:
                return

    def _search_predicates(self, config: SearchConfiguration) -> Optional[List[PRED_CURIE]]:
        """Map the configured search properties onto predicates KGF can filter on.

        ``LABEL`` resolves to whichever predicates the bundle declares as playing the
        ``label`` role, which is what makes search work the same way on bundles that
        name things with something other than ``rdfs:label``.

        :param config: the search configuration
        :return: predicates to restrict the search to, or None to search every predicate
        """
        properties = list(config.properties or [])
        if any(_enum_name(p) == SearchProperty.ANYTHING.text for p in properties):
            return None
        if not properties:
            properties = list(DEFAULT_SEARCH_PROPERTIES)
        predicates = []
        for prop in properties:
            name = _enum_name(prop)
            if name == SearchProperty.LABEL.text:
                predicates.extend(self._label_predicates())
            elif name == SearchProperty.ALIAS.text:
                predicates.extend(self._label_predicates() + SYNONYM_PREDICATES)
            elif name == SearchProperty.DEFINITION.text:
                predicates.extend(DEFINITION_PREDICATES)
            elif name == SearchProperty.COMMENT.text:
                predicates.append(RDFS_COMMENT)
            else:
                logger.warning(f"KGF search cannot filter on {name}; ignoring")
        return list(dict.fromkeys(predicates)) or None

    def _starts_with_search(
        self, search_term: str, predicates: Optional[List[PRED_CURIE]], limit: Optional[int]
    ) -> Iterator[CURIE]:
        """Find entities carrying a literal that starts with ``search_term``.

        KGF stores terms in sorted order and its ``terms`` operation scans them by byte
        prefix, so finding the matching literals is one cheap request. Joining each
        literal back to its subjects then costs one triple pattern request per literal,
        which is why at most :attr:`starts_with_scan_limit` literals are considered.

        The scan is over stored bytes, so unlike the full-text index it is case
        sensitive.

        :param search_term: prefix to match
        :param predicates: predicates the matching literal must be attached by
        :param limit: stop after this many entities
        """
        wanted = set(predicates or self._label_predicates())
        seen = set()
        n = 0
        # literals are stored quoted, so a literal's prefix includes the opening quote
        prefix = f'"{_escape_literal(search_term)}'
        literals = self._paged(
            "terms", {"prefix": prefix, "role": "object"}, limit=self.starts_with_scan_limit
        )
        for term in literals:
            node = term.get("term") or {}
            if node.get("type") != "literal":
                continue
            object_term = _literal_term(self._value(node), lang=node.get("lang"))
            for row in self._paged("fragment", {"o": object_term}):
                if self._curie(row["p"]) not in wanted:
                    continue
                subject = row["s"]
                if _is_blank(subject):
                    continue
                curie = self._curie(subject)
                if curie is None or curie in seen:
                    continue
                seen.add(curie)
                yield curie
                n += 1
                if limit is not None and n >= limit:
                    return
