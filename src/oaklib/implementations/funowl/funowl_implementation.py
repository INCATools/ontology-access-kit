import itertools
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Set, Tuple, Union, cast

import pyhornedowl
import rdflib
import sssom_schema as sssom
from kgcl_schema.datamodel import kgcl
from pyhornedowl.model import (
    IRI,
    AnnotatedComponent,
    Annotation,
    AnnotationAssertion,
    ClassAssertion,
    Component,
    DatatypeLiteral,
    DeclareAnnotationProperty,
    DeclareClass,
    DeclareDataProperty,
    DeclareDatatype,
    DeclareNamedIndividual,
    DeclareObjectProperty,
    DisjointClasses,
    EquivalentClasses,
    InverseObjectProperties,
    LanguageLiteral,
    ObjectHasValue,
    ObjectIntersectionOf,
    ObjectPropertyAssertion,
    ObjectPropertyDomain,
    ObjectPropertyRange,
    ObjectSomeValuesFrom,
    OntologyAnnotation,
    SimpleLiteral,
    SubClassOf,
    SubObjectPropertyOf,
    TransitiveObjectProperty,
)

from oaklib.datamodels import obograph
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchTermSyntax
from oaklib.datamodels.vocabulary import (
    DEPRECATED_PREDICATE,
    EQUIVALENT_CLASS,
    HAS_BROAD_SYNONYM,
    HAS_DBXREF,
    HAS_DEFINITION_CURIE,
    HAS_EXACT_SYNONYM,
    HAS_NARROW_SYNONYM,
    HAS_OBSOLESCENCE_REASON,
    HAS_RELATED_SYNONYM,
    HAS_SYNONYM_TYPE,
    IN_SUBSET,
    INVERSE_OF,
    IS_A,
    LABEL_PREDICATE,
    OWL_ANNOTATION_PROPERTY,
    OWL_CLASS,
    OWL_DATATYPE_PROPERTY,
    OWL_NAMED_INDIVIDUAL,
    OWL_OBJECT_PROPERTY,
    OWL_TRANSITIVE_PROPERTY,
    RDF_TYPE,
    RDFS_COMMENT,
    RDFS_DOMAIN,
    RDFS_RANGE,
    SEMAPV,
    SKOS_MATCH_PREDICATES,
    SUBPROPERTY_OF,
    TERM_REPLACED_BY,
    TERMS_MERGED,
)
from oaklib.interfaces import SearchInterface
from oaklib.interfaces.basic_ontology_interface import LANGUAGE_TAG, RELATIONSHIP
from oaklib.interfaces.dumper_interface import DumperInterface
from oaklib.interfaces.mapping_provider_interface import MappingProviderInterface
from oaklib.interfaces.obograph_interface import GraphTraversalMethod, OboGraphInterface
from oaklib.interfaces.owl_interface import OwlInterface, ReasonerConfiguration
from oaklib.interfaces.patcher_interface import PatcherInterface
from oaklib.interfaces.summary_statistics_interface import SummaryStatisticsInterface
from oaklib.interfaces.text_annotator_interface import TextAnnotatorInterface
from oaklib.types import CURIE, PRED_CURIE, SUBSET_CURIE
from oaklib.utilities.axioms.logical_definition_utilities import logical_definition_matches
from oaklib.utilities.identifier_utils import synonym_type_code_from_curie
from oaklib.utilities.mapping.sssom_utils import inject_mapping_sources

logger = logging.getLogger(__name__)
SERIALIZATION_ALIASES = {
    "functional": "ofn",
    "functional-owl": "ofn",
    "functional-syntax": "ofn",
    "funowl": "ofn",
    "manchester": "ofn",
    "omn": "ofn",
    "ofn": "ofn",
    "owl": "owl",
    "owl-xml": "owx",
    "owl/xml": "owx",
    "owlxml": "owx",
    "owx": "owx",
    "rdf": "rdf",
    "rdf-xml": "rdf",
    "rdf/xml": "rdf",
    "rdfxml": "rdf",
    "xml": "rdf",
}
DECLARATION_TYPES = (
    DeclareClass,
    DeclareObjectProperty,
    DeclareAnnotationProperty,
    DeclareDataProperty,
    DeclareNamedIndividual,
    DeclareDatatype,
)
DECLARATION_TO_OWL_TYPE = {
    DeclareClass: OWL_CLASS,
    DeclareObjectProperty: OWL_OBJECT_PROPERTY,
    DeclareAnnotationProperty: OWL_ANNOTATION_PROPERTY,
    DeclareDataProperty: OWL_DATATYPE_PROPERTY,
    DeclareNamedIndividual: OWL_NAMED_INDIVIDUAL,
}
LITERAL_TYPES = (SimpleLiteral, DatatypeLiteral, LanguageLiteral)
RELATIONSHIP_EXCLUDED_FROM_INHERITANCE = {
    EQUIVALENT_CLASS,
    INVERSE_OF,
    IS_A,
    RDF_TYPE,
    RDFS_DOMAIN,
    RDFS_RANGE,
    SUBPROPERTY_OF,
}
SYNONYM_PREDICATES = [
    HAS_EXACT_SYNONYM,
    HAS_NARROW_SYNONYM,
    HAS_RELATED_SYNONYM,
    HAS_BROAD_SYNONYM,
]
XSD_BOOLEAN = "http://www.w3.org/2001/XMLSchema#boolean"
XSD_STRING_CURIE = "xsd:string"
RDF_LANGSTRING_CURIE = "rdf:langString"
#: syntaxes that py-horned-owl cannot write; these are routed via OBO Graphs
NON_OWL_DUMP_SYNTAXES = {"json", "obojson", "obographs", "obo", "fhirjson", "cx"}


@dataclass(frozen=True)
class ProjectedRelationship:
    subject: CURIE
    predicate: PRED_CURIE
    object: CURIE
    scope: str

    def as_tuple(self) -> RELATIONSHIP:
        return self.subject, self.predicate, self.object


AdjacencyMap = Dict[CURIE, Set[CURIE]]
AdjacencyIndex = Dict[Optional[PRED_CURIE], AdjacencyMap]


@dataclass
class FunOwlImplementation(
    OwlInterface,
    OboGraphInterface,
    DumperInterface,
    PatcherInterface,
    SearchInterface,
    MappingProviderInterface,
    SummaryStatisticsInterface,
    TextAnnotatorInterface,
):
    """
    An experimental partial implementation of :ref:`OwlInterface`

    This adapter keeps the historical ``funowl`` selector and class name for
    backward compatibility, but it now uses py-horned-owl as the OWL parser and
    object model.
    """

    ontology_document: Optional[pyhornedowl.PyIndexedOntology] = None
    _direct_relationship_cache: Optional[List[ProjectedRelationship]] = field(
        default=None, init=False, repr=False
    )
    _entailed_relationship_cache: Optional[List[ProjectedRelationship]] = field(
        default=None, init=False, repr=False
    )
    _direct_outgoing_adjacency_cache: Optional[AdjacencyIndex] = field(
        default=None, init=False, repr=False
    )
    _direct_incoming_adjacency_cache: Optional[AdjacencyIndex] = field(
        default=None, init=False, repr=False
    )
    _entailed_outgoing_adjacency_cache: Optional[AdjacencyIndex] = field(
        default=None, init=False, repr=False
    )
    _entailed_incoming_adjacency_cache: Optional[AdjacencyIndex] = field(
        default=None, init=False, repr=False
    )
    _metadata_map_cache: Dict[CURIE, Dict[PRED_CURIE, List[str]]] = field(
        default_factory=dict, init=False, repr=False
    )
    _owl_type_map_cache: Optional[Dict[CURIE, Set[CURIE]]] = field(
        default=None, init=False, repr=False
    )
    _annotation_index_cache: Optional[Dict[CURIE, List[AnnotatedComponent]]] = field(
        default=None, init=False, repr=False
    )
    _label_index_cache: Optional[Dict[str, List[CURIE]]] = field(
        default=None, init=False, repr=False
    )
    _subproperty_descendant_cache: Optional[Dict[PRED_CURIE, Set[PRED_CURIE]]] = field(
        default=None, init=False, repr=False
    )
    _reported_multivalued: Set[Tuple[CURIE, PRED_CURIE]] = field(
        default_factory=set, init=False, repr=False
    )

    def __post_init__(self):
        resource = self.resource
        local_path = None if resource is None else resource.local_path
        if self.ontology_document is None:
            if local_path is None:
                doc = pyhornedowl.PyIndexedOntology()
            else:
                local_path = Path(local_path)
                logger.info("Loading %s into py-horned-owl", local_path)
                serialization = self._serialization_for_path(local_path)
                if resource is not None and serialization is not None:
                    resource.format = serialization
                doc = pyhornedowl.open_ontology_from_file(
                    str(local_path), serialization=serialization
                )
                if serialization == "ofn":
                    self.prefix_map().update(self._extract_prefix_declarations(local_path))
                else:
                    self.prefix_map().update(self._extract_prefixes_from_rdf(local_path))
            self.ontology_document = doc
        self.functional_writer = self.ontology_document

    def _serialization_for_path(self, path: Path) -> Optional[str]:
        explicit_format = None if self.resource is None else self.resource.format
        serialization = self._normalize_serialization(explicit_format)
        if serialization is not None:
            return serialization
        return self._sniff_serialization(path)

    @staticmethod
    def _normalize_serialization(format_name: Optional[str]) -> Optional[str]:
        if format_name is None:
            return None
        key = format_name.strip().lower().replace("_", "-").replace(" ", "-")
        return SERIALIZATION_ALIASES.get(key, key)

    @staticmethod
    def _sniff_serialization(path: Path) -> Optional[str]:
        suffix = path.suffix.lower()
        if suffix in {".ofn", ".omn"}:
            return "ofn"
        if suffix == ".owx":
            return "owx"
        if suffix not in {".owl", ".rdf", ".xml"}:
            return None
        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:4096]
        except OSError:
            logger.debug("Could not sniff OWL serialization for %s", path, exc_info=True)
            return None
        head = head.lstrip("\ufeff \t\r\n")
        if head.startswith("Prefix(") or head.startswith("Ontology("):
            return "ofn"
        if re.match(r"<Ontology(?:\s|>)", head):
            return "owx"
        if head.startswith("<?xml") or head.startswith("<rdf:RDF") or "xmlns:rdf=" in head:
            return "rdf"
        return None

    @staticmethod
    def _extract_prefix_declarations(path: Path) -> Mapping[str, str]:
        prefix_map: Dict[str, str] = {}
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"Prefix\(\s*([^=]+?)\s*=\s*<([^>]+)>\s*\)", text):
            prefix = match.group(1).strip()
            if prefix.endswith(":"):
                prefix = prefix[:-1]
            prefix_map[prefix] = match.group(2)
        return prefix_map

    @staticmethod
    def _extract_prefixes_from_rdf(path: Path) -> Mapping[str, str]:
        prefix_map: Dict[str, str] = {}
        graph = rdflib.Graph()
        try:
            graph.parse(str(path))
        except Exception:
            try:
                graph.parse(str(path), format="xml")
            except Exception:
                logger.debug("Could not extract RDF prefixes from %s", path, exc_info=True)
                return prefix_map
        for prefix, namespace in graph.namespaces():
            if prefix in {None, ""}:
                continue
            prefix_map[prefix] = str(namespace)
        if path.suffix in {".owl", ".rdf", ".xml"}:
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r'xmlns:([A-Za-z_][\w.-]*)="([^"]+)"', text):
                prefix_map[match.group(1)] = match.group(2)
        return prefix_map

    @property
    def _ontology(self) -> pyhornedowl.PyIndexedOntology:
        return self.ontology_document

    def owl_ontology(self) -> pyhornedowl.PyIndexedOntology:
        return self._ontology

    def _invalidate_caches(self) -> None:
        self._clear_relationship_index()
        self._entailed_edge_index = None
        self._direct_relationship_cache = None
        self._entailed_relationship_cache = None
        self._direct_outgoing_adjacency_cache = None
        self._direct_incoming_adjacency_cache = None
        self._entailed_outgoing_adjacency_cache = None
        self._entailed_incoming_adjacency_cache = None
        self._metadata_map_cache.clear()
        self._owl_type_map_cache = None
        self._annotation_index_cache = None
        self._label_index_cache = None
        self._subproperty_descendant_cache = None

    def _sync_prefix_mapping(self, curie: CURIE) -> None:
        if ":" not in curie:
            return
        prefix, _, _ = curie.partition(":")
        if prefix in self.prefix_map():
            try:
                self._ontology.add_prefix_mapping(prefix, self.prefix_map()[prefix])
            except Exception:
                logger.debug("Could not sync prefix mapping for %s", prefix, exc_info=True)

    def entity_iri_to_curie(self, entity: IRI) -> CURIE:
        return cast(CURIE, self.uri_to_curie(str(entity), use_uri_fallback=True))

    def curie_to_entity_iri(self, curie: CURIE) -> IRI:
        self._sync_prefix_mapping(curie)
        return IRI.parse(self.curie_to_uri(curie))

    def curie_to_class(self, curie: CURIE):
        self._sync_prefix_mapping(curie)
        return self._ontology.clazz(self.curie_to_uri(curie))

    def curie_to_object_property(self, curie: CURIE):
        self._sync_prefix_mapping(curie)
        return self._ontology.object_property(self.curie_to_uri(curie))

    def curie_to_annotation_property(self, curie: CURIE):
        self._sync_prefix_mapping(curie)
        return self._ontology.annotation_property(self.curie_to_uri(curie))

    def _named_curie(self, entity: Any) -> Optional[CURIE]:
        iri = self._entity_iri(entity)
        if iri is None:
            return None
        return self.entity_iri_to_curie(iri)

    def _annotation_value(self, value: Any) -> Optional[str]:
        iri = self._entity_iri(value)
        if iri is not None:
            return self.entity_iri_to_curie(iri)
        literal = self._literal_value(value)
        if literal is None:
            return None
        if isinstance(value, DatatypeLiteral) and str(value.datatype_iri) == XSD_BOOLEAN:
            # align with the SQL adapter, which reports owl:deprecated as a bool
            return literal.lower() in {"1", "true", "yes"}
        return literal

    @staticmethod
    def _is_truthy(values: Iterable[Any]) -> bool:
        return any(
            value is True or (isinstance(value, str) and value.lower() in {"1", "true", "yes"})
            for value in values
        )

    @staticmethod
    def _merge_scopes(left: str, right: str) -> str:
        return "abox" if "abox" in {left, right} else "tbox"

    def _coerce_annotation_value(self, value: Any):
        if isinstance(value, LITERAL_TYPES) or isinstance(value, IRI):
            return value
        if isinstance(value, bool):
            return DatatypeLiteral(str(value).lower(), IRI.parse(XSD_BOOLEAN))
        return SimpleLiteral(str(value))

    def _annotation_assertion_index(self) -> Dict[CURIE, List[AnnotatedComponent]]:
        """Index every ``AnnotationAssertion`` axiom by the CURIE of its subject.

        py-horned-owl exposes axioms as a flat collection, so answering "what is
        asserted about entity X?" by scanning is O(size of ontology) *per entity*.
        Bulk operations such as :meth:`entities` (which filters obsoletes) or
        :meth:`labels` over every term then become quadratic. Building this index
        once makes each lookup a dictionary access.

        The index is invalidated by :meth:`_invalidate_caches` whenever the
        ontology is patched.

        :return: mapping between subject CURIE and the annotated axioms about it
        """
        if self._annotation_index_cache is None:
            index: Dict[CURIE, List[AnnotatedComponent]] = defaultdict(list)
            for annotated in self._ontology.get_axioms():
                component = annotated.component
                if not isinstance(component, AnnotationAssertion):
                    continue
                subject_curie = self._named_curie(component.subject)
                if subject_curie is not None:
                    index[subject_curie].append(annotated)
            self._annotation_index_cache = dict(index)
        return self._annotation_index_cache

    def annotation_assertion_axioms(
        self, subject: Optional[CURIE] = None, property: Optional[CURIE] = None, value: Any = None
    ) -> Iterable[AnnotationAssertion]:
        if subject is None:
            yield from super().annotation_assertion_axioms(
                subject=subject, property=property, value=value
            )
            return
        for annotated in self._annotation_assertion_index().get(subject, []):
            axiom = annotated.component
            if property is not None and not self._entity_matches(axiom.ann.ap, property):
                continue
            if value is not None and not self._entity_matches(axiom.ann.av, value):
                continue
            yield axiom

    def _axiom_annotation_map(self, annotated: AnnotatedComponent) -> Dict[PRED_CURIE, List[str]]:
        """Return the annotations *on* an axiom (e.g. the xrefs on a definition)."""
        annotation_map: Dict[PRED_CURIE, List[str]] = defaultdict(list)
        for annotation in annotated.ann or []:
            predicate = self._named_curie(annotation.ap)
            value = self._annotation_value(annotation.av)
            if predicate is None or value is None:
                continue
            annotation_map[predicate].append(value)
        return dict(annotation_map)

    def _annotation_axioms_for(self, curie: CURIE, property: CURIE) -> Iterator[AnnotatedComponent]:
        for annotated in self._annotation_assertion_index().get(curie, []):
            if self._named_curie(annotated.component.ann.ap) == property:
                yield annotated

    def _single_valued_assignment(self, curie: CURIE, property: CURIE) -> Optional[str]:
        values = self.entity_metadata_map(curie).get(property, [])
        if values:
            if len(values) > 1 and (curie, property) not in self._reported_multivalued:
                # warn once per entity/property: label() is called in tight loops
                self._reported_multivalued.add((curie, property))
                logger.warning("Multiple values for %s %s = %s", curie, property, values)
            return values[0]
        return None

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        return self._single_valued_assignment(curie, HAS_DEFINITION_CURIE)

    def definitions(
        self,
        curies: Iterable[CURIE],
        include_metadata=False,
        include_missing=False,
        lang: Optional[LANGUAGE_TAG] = None,
    ) -> Iterator[Tuple[CURIE, Optional[str], Dict]]:
        for curie in curies:
            definition = self.definition(curie, lang=lang)
            if not definition and not include_missing:
                continue
            metadata: Dict[PRED_CURIE, List[str]] = {}
            if include_metadata:
                for annotated in self._annotation_axioms_for(curie, HAS_DEFINITION_CURIE):
                    metadata = self._axiom_annotation_map(annotated)
                    break
            yield curie, definition, metadata

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        return self._single_valued_assignment(curie, LABEL_PREDICATE)

    def _label_index(self) -> Dict[str, List[CURIE]]:
        if self._label_index_cache is None:
            index: Dict[str, List[CURIE]] = defaultdict(list)
            for curie in self.entities(filter_obsoletes=False):
                label = self.label(curie)
                if label is not None:
                    index[label].append(curie)
            self._label_index_cache = dict(index)
        return self._label_index_cache

    def curies_by_label(self, label: str) -> List[CURIE]:
        return list(self._label_index().get(label, []))

    def _owl_type_map(self) -> Dict[CURIE, Set[CURIE]]:
        if self._owl_type_map_cache is None:
            type_map: Dict[CURIE, Set[CURIE]] = defaultdict(set)
            for axiom in self._ontology.get_axioms():
                component = axiom.component
                for declaration_type, owl_type in DECLARATION_TO_OWL_TYPE.items():
                    if isinstance(component, declaration_type):
                        curie = self._named_curie(component.first)
                        if curie is not None:
                            type_map[curie].add(owl_type)
                        break
                if isinstance(component, TransitiveObjectProperty):
                    curie = self._named_curie(component.first)
                    if curie is not None:
                        type_map[curie].add(OWL_OBJECT_PROPERTY)
                        type_map[curie].add(OWL_TRANSITIVE_PROPERTY)
            self._owl_type_map_cache = {curie: set(types) for curie, types in type_map.items()}
        return self._owl_type_map_cache

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        seen = set()
        obsolete_set = set(self.obsoletes()) if filter_obsoletes else set()
        type_map = self._owl_type_map()
        for axiom in self._ontology.get_axioms():
            component = axiom.component
            if not isinstance(component, DECLARATION_TYPES):
                continue
            curie = self._named_curie(component.first)
            if curie is None or curie in seen:
                continue
            seen.add(curie)
            if curie in obsolete_set:
                continue
            if owl_type is None or owl_type in type_map.get(curie, set()):
                yield curie

    def ontologies(self) -> Iterable[CURIE]:
        iri = self._ontology.get_iri()
        if iri is None:
            return
        yield cast(CURIE, self.uri_to_curie(str(iri), use_uri_fallback=True))

    def ontology_metadata_map(self, ontology: CURIE) -> Dict[PRED_CURIE, List[str]]:
        metadata_map: Dict[PRED_CURIE, List[str]] = defaultdict(list)
        for annotated in self._ontology.get_components():
            component = annotated.component
            if not isinstance(component, OntologyAnnotation):
                continue
            predicate = self._named_curie(component.first.ap)
            value = self._annotation_value(component.first.av)
            if predicate is None or value is None:
                continue
            metadata_map[predicate].append(value)
        # ontology-level assertions may also be made about the ontology IRI itself
        for predicate, values in self.entity_metadata_map(ontology).items():
            metadata_map[predicate].extend(values)
        return dict(metadata_map)

    def ontology_versions(self, ontology: CURIE) -> Iterable[str]:
        version_iri = self._ontology.get_version_iri()
        if version_iri is not None:
            yield str(version_iri)

    def owl_types(self, entities: Iterable[CURIE]) -> Iterable[tuple[CURIE, CURIE]]:
        type_map = self._owl_type_map()
        for curie in entities:
            for owl_type in sorted(type_map.get(curie, set())):
                yield curie, owl_type

    def obsoletes(self, include_merged=True) -> Iterable[CURIE]:
        for curie in self.entities(filter_obsoletes=False):
            metadata = self.entity_metadata_map(curie)
            if not self._is_truthy(metadata.get(DEPRECATED_PREDICATE, [])):
                continue
            if not include_merged and TERMS_MERGED in metadata.get(HAS_OBSOLESCENCE_REASON, []):
                continue
            yield curie

    def entity_metadata_map(self, curie: CURIE) -> Dict[PRED_CURIE, List[str]]:
        if curie not in self._metadata_map_cache:
            metadata_map: Dict[PRED_CURIE, List[str]] = defaultdict(list)
            for annotated in self._annotation_assertion_index().get(curie, []):
                axiom = annotated.component
                predicate = self._named_curie(axiom.ann.ap)
                value = self._annotation_value(axiom.ann.av)
                if predicate is None or value is None:
                    continue
                metadata_map[predicate].append(value)
            self._metadata_map_cache[curie] = dict(metadata_map)
        return self._metadata_map_cache[curie]

    def entities_metadata_statements(
        self,
        curies: Iterable[CURIE],
        predicates: Optional[List[PRED_CURIE]] = None,
        include_nested_metadata=False,
        **kwargs,
    ) -> Iterator[Tuple[CURIE, PRED_CURIE, str, Optional[str], Dict]]:
        predicate_set = set(predicates) if predicates is not None else None
        for curie in curies:
            for annotated in self._annotation_assertion_index().get(curie, []):
                axiom = annotated.component
                predicate = self._named_curie(axiom.ann.ap)
                value = self._annotation_value(axiom.ann.av)
                if predicate is None or value is None:
                    continue
                if predicate_set is not None and predicate not in predicate_set:
                    continue
                datatype = self._annotation_datatype(axiom.ann.av)
                nested = self._axiom_annotation_map(annotated) if include_nested_metadata else {}
                yield curie, predicate, value, datatype, nested

    def _annotation_datatype(self, value: Any) -> Optional[str]:
        """Return the CURIE for the datatype of an annotation value, if it is a literal."""
        if isinstance(value, DatatypeLiteral):
            return self.uri_to_curie(str(value.datatype_iri), use_uri_fallback=True)
        if isinstance(value, SimpleLiteral):
            return XSD_STRING_CURIE
        if isinstance(value, LanguageLiteral):
            return RDF_LANGSTRING_CURIE
        return None

    def entity_alias_map(self, curie: CURIE) -> Dict[PRED_CURIE, List[str]]:
        alias_map: Dict[PRED_CURIE, List[str]] = defaultdict(list)
        metadata = self.entity_metadata_map(curie)
        # an entity may carry more than one rdfs:label (e.g. "part of" and "part_of");
        # all of them are aliases, even though only one is returned by label()
        labels = [value for value in metadata.get(LABEL_PREDICATE, []) if isinstance(value, str)]
        if labels:
            alias_map[LABEL_PREDICATE].extend(labels)
        for predicate in SYNONYM_PREDICATES:
            values = metadata.get(predicate, [])
            if values:
                alias_map[predicate].extend(values)
        return dict(alias_map)

    @staticmethod
    def _subset_code(subset: str) -> SUBSET_CURIE:
        """Compact ``obo:go#goslim_generic`` down to ``goslim_generic``."""
        if "#" in subset:
            return cast(SUBSET_CURIE, subset.split("#")[-1])
        return cast(SUBSET_CURIE, subset)

    def terms_subsets(self, curies: Iterable[CURIE]) -> Iterable[Tuple[CURIE, SUBSET_CURIE]]:
        for curie in curies:
            for subset in self.entity_metadata_map(curie).get(IN_SUBSET, []):
                yield curie, self._subset_code(subset)

    def subsets(self) -> Iterable[SUBSET_CURIE]:
        seen = set()
        for _, subset in self.terms_subsets(self.entities(filter_obsoletes=False)):
            if subset not in seen:
                seen.add(subset)
                yield subset

    def subset_members(self, subset: SUBSET_CURIE) -> Iterable[CURIE]:
        for curie, curie_subset in self.terms_subsets(self.entities(filter_obsoletes=False)):
            if curie_subset == subset:
                yield curie

    def synonym_property_values(
        self, subject: CURIE | Iterable[CURIE]
    ) -> Iterator[tuple[CURIE, obograph.SynonymPropertyValue]]:
        subjects = [subject] if isinstance(subject, str) else list(subject)
        for curie in subjects:
            for predicate in SYNONYM_PREDICATES:
                pred_text = predicate.split(":")[-1]
                for annotated in self._annotation_axioms_for(curie, predicate):
                    value = self._annotation_value(annotated.component.ann.av)
                    if value is None:
                        continue
                    spv = obograph.SynonymPropertyValue(pred=pred_text, val=value)
                    self._decorate_property_value(spv, self._axiom_annotation_map(annotated))
                    yield curie, spv

    def _decorate_property_value(
        self, pv: obograph.PropertyValue, annotations: Dict[PRED_CURIE, List[str]]
    ) -> None:
        """Attach axiom annotations (xrefs, synonym type, other) to an obograph value."""
        xrefs = annotations.get(HAS_DBXREF, [])
        if xrefs:
            pv.xrefs = list(xrefs)
        if isinstance(pv, obograph.SynonymPropertyValue):
            synonym_types = annotations.get(HAS_SYNONYM_TYPE, [])
            if synonym_types:
                pv.synonymType = synonym_type_code_from_curie(synonym_types[0])
                if len(synonym_types) > 1:
                    logger.warning("Ignoring multiple synonym types: %s", synonym_types)
        basic_property_values = [
            obograph.BasicPropertyValue(pred=predicate, val=value)
            for predicate, values in annotations.items()
            if predicate != HAS_DBXREF
            for value in values
        ]
        if basic_property_values:
            pv.meta = obograph.Meta(basicPropertyValues=basic_property_values)

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[tuple[PRED_CURIE, CURIE]]:
        metadata = self.entity_metadata_map(curie)
        for xref in metadata.get(HAS_DBXREF, []):
            yield HAS_DBXREF, cast(CURIE, xref)
        for predicate in SKOS_MATCH_PREDICATES:
            for mapped_curie in metadata.get(predicate, []):
                yield predicate, cast(CURIE, mapped_curie)

    def get_sssom_mappings_by_curie(self, curie: CURIE) -> Iterable[sssom.Mapping]:
        seen = set()

        def _mapping(
            subject_id: CURIE, predicate_id: PRED_CURIE, object_id: CURIE
        ) -> sssom.Mapping:
            mapping = sssom.Mapping(
                subject_id=subject_id,
                predicate_id=predicate_id,
                object_id=object_id,
                mapping_justification=sssom.EntityReference(SEMAPV.UnspecifiedMatching.value),
            )
            inject_mapping_sources(mapping)
            return mapping

        direct_mappings = list(self.simple_mappings_by_curie(curie))
        for predicate_id, object_id in direct_mappings:
            key = (curie, predicate_id, object_id)
            if key in seen:
                continue
            seen.add(key)
            yield _mapping(curie, predicate_id, object_id)

        if direct_mappings or self.label(curie) is not None or set(self.owl_type(curie)):
            return

        for entity in self.entities(filter_obsoletes=False):
            for predicate_id, object_id in self.simple_mappings_by_curie(entity):
                if object_id != curie:
                    continue
                key = (entity, predicate_id, object_id)
                if key in seen:
                    continue
                seen.add(key)
                yield _mapping(entity, predicate_id, object_id)

    def basic_search(
        self, search_term: str, config: Optional[SearchConfiguration] = None
    ) -> Iterable[CURIE]:
        if config is None:
            config = SearchConfiguration()
        property_names = {str(p) for p in config.properties}
        if not property_names:
            property_names = {"LABEL", "ALIAS"}

        flags = re.IGNORECASE if config.force_case_insensitive else 0
        normalized_search_term = (
            search_term.lower() if config.force_case_insensitive else search_term
        )

        def _normalize(value: str) -> str:
            return value.lower() if config.force_case_insensitive else value

        if config.syntax == SearchTermSyntax(SearchTermSyntax.STARTS_WITH):
            matches = lambda value: _normalize(value).startswith(normalized_search_term)
        elif config.syntax == SearchTermSyntax(SearchTermSyntax.REGULAR_EXPRESSION):
            prog = re.compile(search_term, flags=flags)
            matches = lambda value: prog.search(value) is not None
        elif config.is_partial:
            matches = lambda value: normalized_search_term in _normalize(value)
        else:
            matches = lambda value: _normalize(value) == normalized_search_term

        search_all = "ANYTHING" in property_names
        seen = set()
        for curie in self.entities(filter_obsoletes=not config.include_obsoletes_in_results):
            if (
                (search_all or "LABEL" in property_names)
                and (label := self.label(curie))
                and matches(label)
            ):
                if curie not in seen:
                    seen.add(curie)
                    yield curie
                continue
            if (search_all or "IDENTIFIER" in property_names) and matches(curie):
                if curie not in seen:
                    seen.add(curie)
                    yield curie
                continue
            if search_all or "ALIAS" in property_names:
                if any(matches(alias) for alias in self.entity_aliases(curie)):
                    if curie not in seen:
                        seen.add(curie)
                        yield curie
                    continue
            if search_all or "MAPPED_IDENTIFIER" in property_names:
                metadata = self.entity_metadata_map(curie)
                if any(matches(xref) for xref in metadata.get(HAS_DBXREF, [])):
                    if curie not in seen:
                        seen.add(curie)
                        yield curie
        if search_all or "REPLACEMENT_IDENTIFIER" in property_names:
            # the search term matches an obsolete entity; the *replacement* is returned
            for curie in self.entities(filter_obsoletes=False):
                if not matches(curie):
                    continue
                for replacement in self.entity_metadata_map(curie).get(TERM_REPLACED_BY, []):
                    if replacement not in seen:
                        seen.add(replacement)
                        yield replacement

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> Optional[obograph.Node]:
        entity_types = set(self.owl_type(curie))
        label = self.label(curie)
        node_id = cast(CURIE, self.curie_to_uri(curie)) if expand_curies else curie
        if node_id is None:
            node_id = curie
        if not entity_types and label is None:
            if strict:
                raise ValueError(f"Unknown entity: {curie}")
            return obograph.Node(id=node_id)
        if any(
            owl_type in entity_types
            for owl_type in [OWL_OBJECT_PROPERTY, OWL_ANNOTATION_PROPERTY, OWL_DATATYPE_PROPERTY]
        ):
            node_type = "PROPERTY"
        elif OWL_NAMED_INDIVIDUAL in entity_types:
            node_type = "INDIVIDUAL"
        else:
            node_type = "CLASS"
        return obograph.Node(
            id=node_id,
            lbl=label,
            type=node_type,
            meta=self._node_meta(curie, include_metadata=include_metadata),
        )

    def _node_meta(self, curie: CURIE, include_metadata=False) -> obograph.Meta:
        """Build the obograph ``Meta`` block for an entity.

        Basic metadata (definition, synonyms, xrefs, subsets, comments) is always
        included; ``include_metadata`` additionally attaches the annotations
        *on* those axioms, e.g. the xrefs supporting a definition or the type of
        a synonym. This mirrors the behaviour of the SQL adapter.
        """
        meta = obograph.Meta()
        metadata_map = self.entity_metadata_map(curie)
        handled_predicates = {
            HAS_DEFINITION_CURIE,
            HAS_DBXREF,
            IN_SUBSET,
            LABEL_PREDICATE,
            RDFS_COMMENT,
            *SYNONYM_PREDICATES,
        }
        for annotated in self._annotation_axioms_for(curie, HAS_DEFINITION_CURIE):
            definition = self._annotation_value(annotated.component.ann.av)
            if not definition:
                continue
            meta.definition = obograph.DefinitionPropertyValue(val=definition)
            if include_metadata:
                self._decorate_property_value(
                    meta.definition, self._axiom_annotation_map(annotated)
                )
            break
        for annotated in self._annotation_axioms_for(curie, HAS_DBXREF):
            xref = self._annotation_value(annotated.component.ann.av)
            if xref is None:
                continue
            pv = obograph.XrefPropertyValue(val=xref)
            if include_metadata:
                self._decorate_property_value(pv, self._axiom_annotation_map(annotated))
            cast(List[obograph.XrefPropertyValue], meta.xrefs).append(pv)
        for comment in metadata_map.get(RDFS_COMMENT, []):
            cast(List[str], meta.comments).append(comment)
        for subset in metadata_map.get(IN_SUBSET, []):
            cast(List[str], meta.subsets).append(subset)
        if self._is_truthy(metadata_map.get(DEPRECATED_PREDICATE, [])):
            meta.deprecated = True
        for _, synonym in self.synonym_property_values([curie]):
            if not include_metadata:
                synonym.xrefs = []
                synonym.meta = None
                synonym.synonymType = None
            cast(List[obograph.SynonymPropertyValue], meta.synonyms).append(synonym)
        for predicate, values in metadata_map.items():
            if predicate in handled_predicates:
                continue
            for value in values:
                cast(List[obograph.BasicPropertyValue], meta.basicPropertyValues).append(
                    obograph.BasicPropertyValue(pred=predicate, val=value)
                )
        return meta

    def logical_definitions(
        self,
        subjects: Optional[Iterable[CURIE]] = None,
        predicates: Optional[Iterable[PRED_CURIE]] = None,
        objects: Optional[Iterable[CURIE]] = None,
        **kwargs,
    ) -> Iterable[obograph.LogicalDefinitionAxiom]:
        subject_set = set(subjects) if subjects is not None else None
        predicate_list = list(predicates) if predicates is not None else None
        object_list = list(objects) if objects is not None else None
        for axiom in self.axioms():
            if not isinstance(axiom, EquivalentClasses):
                continue
            expressions = list(axiom.first)
            if len(expressions) != 2:
                continue
            defined_class = None
            intersection = None
            for expression in expressions:
                curie = self._named_curie(expression)
                if curie is not None:
                    defined_class = curie
                elif isinstance(expression, ObjectIntersectionOf):
                    intersection = expression
            if defined_class is None or intersection is None:
                continue
            if subject_set is not None and defined_class not in subject_set:
                continue
            ldef = obograph.LogicalDefinitionAxiom(definedClassId=defined_class)
            valid = True
            for expression in intersection.first:
                genus = self._named_curie(expression)
                if genus is not None:
                    cast(List[CURIE], ldef.genusIds).append(genus)
                    continue
                if isinstance(expression, ObjectSomeValuesFrom):
                    predicate = self._named_curie(expression.ope)
                    filler = self._named_curie(expression.bce)
                    if predicate is None or filler is None:
                        valid = False
                        break
                    cast(
                        List[obograph.ExistentialRestrictionExpression],
                        ldef.restrictions,
                    ).append(
                        obograph.ExistentialRestrictionExpression(
                            propertyId=predicate,
                            fillerId=filler,
                        )
                    )
                    continue
                valid = False
                break
            if valid and logical_definition_matches(
                ldef, predicates=predicate_list, objects=object_list
            ):
                yield ldef

    def axioms(self, reasoner: Optional[ReasonerConfiguration] = None) -> Iterable[Component]:
        for axiom in self._ontology.get_axioms():
            yield axiom.component

    def disjoint_pairs(
        self, subjects: Optional[Iterable[CURIE]] = None
    ) -> Iterable[Tuple[CURIE, CURIE]]:
        subject_set = set(subjects) if subjects is not None else None
        for axiom in self.axioms():
            if not isinstance(axiom, DisjointClasses):
                continue
            curies = [self._named_curie(expression) for expression in axiom.first]
            named = [curie for curie in curies if curie is not None]
            for left, right in itertools.combinations(named, 2):
                if subject_set is None or left in subject_set or right in subject_set:
                    yield left, right

    def is_disjoint(self, subject: CURIE, object: CURIE, bidirectional=True) -> bool:
        """Test whether two entities are asserted or entailed to be disjoint.

        Two classes are entailed disjoint if any of their (reflexive) is-a
        ancestors are asserted disjoint from each other.
        """
        subject_ancestors = set(self.ancestors(subject, predicates=[IS_A], reflexive=True))
        object_ancestors = set(self.ancestors(object, predicates=[IS_A], reflexive=True))
        for left, right in self.disjoint_pairs():
            if left in subject_ancestors and right in object_ancestors:
                return True
            if bidirectional and right in subject_ancestors and left in object_ancestors:
                return True
        return False

    def _project_axiom_relationships(self, axiom: Component) -> Iterator[ProjectedRelationship]:
        if isinstance(axiom, SubClassOf):
            subject = self._named_curie(axiom.sub)
            if subject is None:
                return
            object_curie = self._named_curie(axiom.sup)
            if object_curie is not None:
                yield ProjectedRelationship(subject, IS_A, object_curie, "tbox")
                return
            if isinstance(axiom.sup, ObjectSomeValuesFrom):
                predicate = self._named_curie(axiom.sup.ope)
                object_curie = self._named_curie(axiom.sup.bce)
                if predicate is not None and object_curie is not None:
                    yield ProjectedRelationship(subject, predicate, object_curie, "tbox")
                return
            if isinstance(axiom.sup, ObjectHasValue):
                predicate = self._named_curie(axiom.sup.ope)
                object_curie = self._named_curie(axiom.sup.i)
                if predicate is not None and object_curie is not None:
                    yield ProjectedRelationship(subject, predicate, object_curie, "abox")
                return
        if isinstance(axiom, EquivalentClasses):
            expressions = [self._named_curie(expression) for expression in axiom.first]
            if len(expressions) == 2 and all(expression is not None for expression in expressions):
                left = cast(CURIE, expressions[0])
                right = cast(CURIE, expressions[1])
                yield ProjectedRelationship(left, EQUIVALENT_CLASS, right, "tbox")
                yield ProjectedRelationship(right, EQUIVALENT_CLASS, left, "tbox")
            return
        if isinstance(axiom, SubObjectPropertyOf):
            subject = self._named_curie(axiom.sub)
            object_curie = self._named_curie(axiom.sup)
            if subject is not None and object_curie is not None:
                yield ProjectedRelationship(subject, SUBPROPERTY_OF, object_curie, "tbox")
            return
        if isinstance(axiom, ObjectPropertyDomain):
            subject = self._named_curie(axiom.ope)
            object_curie = self._named_curie(axiom.ce)
            if subject is not None and object_curie is not None:
                yield ProjectedRelationship(subject, RDFS_DOMAIN, object_curie, "tbox")
            return
        if isinstance(axiom, ObjectPropertyRange):
            subject = self._named_curie(axiom.ope)
            object_curie = self._named_curie(axiom.ce)
            if subject is not None and object_curie is not None:
                yield ProjectedRelationship(subject, RDFS_RANGE, object_curie, "tbox")
            return
        if isinstance(axiom, InverseObjectProperties):
            first = self._named_curie(axiom.first)
            second = self._named_curie(axiom.second)
            if first is not None and second is not None:
                yield ProjectedRelationship(first, INVERSE_OF, second, "tbox")
                yield ProjectedRelationship(second, INVERSE_OF, first, "tbox")
            return
        if isinstance(axiom, ClassAssertion):
            subject = self._named_curie(axiom.i)
            if subject is None:
                return
            object_curie = self._named_curie(axiom.ce)
            if object_curie is not None:
                yield ProjectedRelationship(subject, RDF_TYPE, object_curie, "abox")
                return
            if isinstance(axiom.ce, ObjectHasValue):
                predicate = self._named_curie(axiom.ce.ope)
                object_curie = self._named_curie(axiom.ce.i)
                if predicate is not None and object_curie is not None:
                    yield ProjectedRelationship(subject, predicate, object_curie, "abox")
            return
        if isinstance(axiom, ObjectPropertyAssertion):
            subject = self._named_curie(axiom.source)
            predicate = self._named_curie(axiom.ope)
            object_curie = self._named_curie(axiom.target)
            if subject is not None and predicate is not None and object_curie is not None:
                yield ProjectedRelationship(subject, predicate, object_curie, "abox")

    def _direct_relationships(self) -> List[ProjectedRelationship]:
        if self._direct_relationship_cache is None:
            seen = set()
            relationships = []
            for axiom in self.axioms():
                for relationship in self._project_axiom_relationships(axiom):
                    if relationship in seen:
                        continue
                    seen.add(relationship)
                    relationships.append(relationship)
            self._direct_relationship_cache = relationships
        return self._direct_relationship_cache

    @staticmethod
    def _transitive_targets(source: CURIE, adjacency_map: Mapping[CURIE, Set[CURIE]]) -> Set[CURIE]:
        stack = list(adjacency_map.get(source, set()))
        targets = set()
        while stack:
            target = stack.pop()
            if target in targets:
                continue
            targets.add(target)
            stack.extend(adjacency_map.get(target, set()).difference(targets))
        return targets

    @staticmethod
    def _as_curie_list(start_curies: Union[CURIE, List[CURIE]]) -> List[CURIE]:
        if isinstance(start_curies, str):
            return [start_curies]
        return list(start_curies)

    @staticmethod
    def _build_adjacency_indexes(
        relationships: Iterable[ProjectedRelationship],
    ) -> Tuple[AdjacencyIndex, AdjacencyIndex]:
        outgoing: AdjacencyIndex = {None: defaultdict(set)}
        incoming: AdjacencyIndex = {None: defaultdict(set)}
        for relationship in relationships:
            outgoing[None][relationship.subject].add(relationship.object)
            incoming[None][relationship.object].add(relationship.subject)
            outgoing.setdefault(relationship.predicate, defaultdict(set))[relationship.subject].add(
                relationship.object
            )
            incoming.setdefault(relationship.predicate, defaultdict(set))[relationship.object].add(
                relationship.subject
            )
        return outgoing, incoming

    def _direct_adjacency_indexes(self) -> Tuple[AdjacencyIndex, AdjacencyIndex]:
        if (
            self._direct_outgoing_adjacency_cache is None
            or self._direct_incoming_adjacency_cache is None
        ):
            (
                self._direct_outgoing_adjacency_cache,
                self._direct_incoming_adjacency_cache,
            ) = self._build_adjacency_indexes(self._direct_relationships())
        return self._direct_outgoing_adjacency_cache, self._direct_incoming_adjacency_cache

    def _entailed_adjacency_indexes(self) -> Tuple[AdjacencyIndex, AdjacencyIndex]:
        if (
            self._entailed_outgoing_adjacency_cache is None
            or self._entailed_incoming_adjacency_cache is None
        ):
            (
                self._entailed_outgoing_adjacency_cache,
                self._entailed_incoming_adjacency_cache,
            ) = self._build_adjacency_indexes(self._entailed_relationships())
        return self._entailed_outgoing_adjacency_cache, self._entailed_incoming_adjacency_cache

    def _subproperty_descendants(self) -> Dict[PRED_CURIE, Set[PRED_CURIE]]:
        """Map each property onto its transitive sub-properties."""
        if self._subproperty_descendant_cache is None:
            children: Dict[PRED_CURIE, Set[PRED_CURIE]] = defaultdict(set)
            for relationship in self._direct_relationships():
                if relationship.predicate == SUBPROPERTY_OF:
                    children[relationship.object].add(relationship.subject)
            self._subproperty_descendant_cache = {
                parent: self._transitive_targets(parent, children) for parent in children
            }
        return self._subproperty_descendant_cache

    def _expand_predicates(self, predicates: Optional[List[PRED_CURIE]]) -> Optional[List[CURIE]]:
        """Expand a predicate list with sub-properties.

        ``C SubClassOf part_of some D`` also entails ``C SubClassOf overlaps some D``
        when ``part_of`` is a sub-property of ``overlaps``, so a walk over
        ``overlaps`` must also follow ``part_of`` edges.
        """
        if predicates is None:
            return None
        descendant_map = self._subproperty_descendants()
        expanded: Set[PRED_CURIE] = set()
        for predicate in predicates:
            expanded.add(predicate)
            expanded.update(descendant_map.get(predicate, set()))
        return sorted(expanded)

    @staticmethod
    def _select_adjacency_map(
        index: AdjacencyIndex, predicates: Optional[List[PRED_CURIE]]
    ) -> Mapping[CURIE, Set[CURIE]]:
        if predicates is None:
            return index.get(None, {})
        if len(predicates) == 1:
            return index.get(predicates[0], {})
        adjacency_map: AdjacencyMap = defaultdict(set)
        for predicate in predicates:
            for source, targets in index.get(predicate, {}).items():
                adjacency_map[source].update(targets)
        return adjacency_map

    def _closure_targets(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: Optional[List[PRED_CURIE]],
        reflexive: bool,
        *,
        incoming: bool,
        include_entailed: bool,
    ) -> List[CURIE]:
        start_curie_list = self._as_curie_list(start_curies)
        outgoing_index, incoming_index = (
            self._entailed_adjacency_indexes()
            if include_entailed
            else self._direct_adjacency_indexes()
        )
        index = incoming_index if incoming else outgoing_index
        adjacency_map = self._select_adjacency_map(index, self._expand_predicates(predicates))
        targets: Set[CURIE] = set()
        for curie in start_curie_list:
            if include_entailed:
                targets.update(adjacency_map.get(curie, set()))
            else:
                targets.update(self._transitive_targets(curie, adjacency_map))
        if reflexive:
            targets.update(start_curie_list)
        else:
            targets.difference_update(start_curie_list)
        return list(targets)

    def ancestors(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: Optional[List[PRED_CURIE]] = None,
        reflexive: bool = True,
        method: Optional[GraphTraversalMethod] = None,
    ) -> Iterable[CURIE]:
        """
        Ancestors obtained from cached predicate adjacency maps.

        This avoids repeatedly scanning the full projected relationship list during
        graph walks over large OWL files.
        """
        return self._closure_targets(
            start_curies,
            predicates,
            reflexive,
            incoming=False,
            include_entailed=method == GraphTraversalMethod.ENTAILMENT,
        )

    def descendants(
        self,
        start_curies: Union[CURIE, List[CURIE]],
        predicates: Optional[List[PRED_CURIE]] = None,
        reflexive: bool = True,
        method: Optional[GraphTraversalMethod] = None,
    ) -> Iterable[CURIE]:
        """
        Descendants obtained from cached predicate adjacency maps.

        This avoids repeatedly scanning the full projected relationship list during
        graph walks over large OWL files.
        """
        return self._closure_targets(
            start_curies,
            predicates,
            reflexive,
            incoming=True,
            include_entailed=method == GraphTraversalMethod.ENTAILMENT,
        )

    def _entailed_relationships(self) -> List[ProjectedRelationship]:
        if self._entailed_relationship_cache is None:
            direct_relationships = self._direct_relationships()
            entailed = set(direct_relationships)
            class_parents: Dict[CURIE, Set[CURIE]] = defaultdict(set)
            property_parents: Dict[CURIE, Set[CURIE]] = defaultdict(set)
            inverse_properties: Dict[CURIE, Set[CURIE]] = defaultdict(set)
            for relationship in direct_relationships:
                if relationship.predicate == IS_A:
                    class_parents[relationship.subject].add(relationship.object)
                elif relationship.predicate == SUBPROPERTY_OF:
                    property_parents[relationship.subject].add(relationship.object)
                elif relationship.predicate == INVERSE_OF:
                    inverse_properties[relationship.subject].add(relationship.object)
                    inverse_properties[relationship.object].add(relationship.subject)
            class_ancestors = {
                subject: self._transitive_targets(subject, class_parents)
                for subject in class_parents
            }
            property_ancestors = {
                subject: self._transitive_targets(subject, property_parents)
                for subject in property_parents
            }
            descendants: Dict[CURIE, Set[CURIE]] = defaultdict(set)
            for subject, ancestors in class_ancestors.items():
                for ancestor in ancestors:
                    descendants[ancestor].add(subject)
            transitive_properties = set(self.transitive_object_properties())

            def add_relationship(relationship: ProjectedRelationship) -> bool:
                if relationship.subject == relationship.object and relationship.predicate in {
                    IS_A,
                    SUBPROPERTY_OF,
                }:
                    return False
                if relationship in entailed:
                    return False
                entailed.add(relationship)
                return True

            changed = True
            while changed:
                changed = False
                current_relationships = list(entailed)
                relationships_by_predicate: Dict[PRED_CURIE, List[ProjectedRelationship]] = (
                    defaultdict(list)
                )
                for relationship in current_relationships:
                    relationships_by_predicate[relationship.predicate].append(relationship)
                for relationship in current_relationships:
                    if relationship.predicate == IS_A:
                        for ancestor in class_ancestors.get(relationship.object, set()):
                            changed |= add_relationship(
                                ProjectedRelationship(
                                    relationship.subject,
                                    IS_A,
                                    ancestor,
                                    "tbox",
                                )
                            )
                    elif relationship.predicate == SUBPROPERTY_OF:
                        for ancestor in property_ancestors.get(relationship.object, set()):
                            changed |= add_relationship(
                                ProjectedRelationship(
                                    relationship.subject,
                                    SUBPROPERTY_OF,
                                    ancestor,
                                    "tbox",
                                )
                            )
                    elif relationship.predicate == RDF_TYPE:
                        for ancestor in class_ancestors.get(relationship.object, set()):
                            changed |= add_relationship(
                                ProjectedRelationship(
                                    relationship.subject,
                                    RDF_TYPE,
                                    ancestor,
                                    relationship.scope,
                                )
                            )
                    if relationship.predicate not in RELATIONSHIP_EXCLUDED_FROM_INHERITANCE:
                        # C SubClassOf R some D, C' SubClassOf C |= C' SubClassOf R some D
                        for descendant in descendants.get(relationship.subject, set()):
                            changed |= add_relationship(
                                ProjectedRelationship(
                                    descendant,
                                    relationship.predicate,
                                    relationship.object,
                                    relationship.scope,
                                )
                            )
                        # C SubClassOf R some D, D SubClassOf D' |= C SubClassOf R some D'
                        for ancestor in class_ancestors.get(relationship.object, set()):
                            changed |= add_relationship(
                                ProjectedRelationship(
                                    relationship.subject,
                                    relationship.predicate,
                                    ancestor,
                                    relationship.scope,
                                )
                            )
                    for ancestor in property_ancestors.get(relationship.predicate, set()):
                        changed |= add_relationship(
                            ProjectedRelationship(
                                relationship.subject,
                                ancestor,
                                relationship.object,
                                relationship.scope,
                            )
                        )
                    if relationship.scope == "abox":
                        # a R b |= b inverse(R) a. This holds for individuals only:
                        # at the class level `C SubClassOf R some D` does *not*
                        # entail `D SubClassOf inverse(R) some C`, and applying it
                        # there makes the closure explode (see the reflexive
                        # `BFO:0000002 part_of BFO:0000002` axiom in go-nucleus).
                        for inverse_predicate in inverse_properties.get(
                            relationship.predicate, set()
                        ):
                            changed |= add_relationship(
                                ProjectedRelationship(
                                    relationship.object,
                                    inverse_predicate,
                                    relationship.subject,
                                    relationship.scope,
                                )
                            )
                for predicate in transitive_properties:
                    adjacency_map: Dict[CURIE, List[tuple[CURIE, str]]] = defaultdict(list)
                    for relationship in relationships_by_predicate.get(predicate, []):
                        adjacency_map[relationship.subject].append(
                            (relationship.object, relationship.scope)
                        )
                    for subject, targets in adjacency_map.items():
                        stack = list(targets)
                        seen = {target for target, _ in targets}
                        while stack:
                            intermediate, scope = stack.pop()
                            for target, target_scope in adjacency_map.get(intermediate, []):
                                if target == subject:
                                    continue
                                merged_scope = self._merge_scopes(scope, target_scope)
                                changed |= add_relationship(
                                    ProjectedRelationship(
                                        subject,
                                        predicate,
                                        target,
                                        merged_scope,
                                    )
                                )
                                if target not in seen:
                                    seen.add(target)
                                    stack.append((target, merged_scope))
            self._entailed_relationship_cache = sorted(
                entailed,
                key=lambda relationship: (
                    relationship.subject,
                    relationship.predicate,
                    relationship.object,
                    relationship.scope,
                ),
            )
        return self._entailed_relationship_cache

    def _filter_relationships(
        self,
        relationships: Iterable[ProjectedRelationship],
        subjects: Optional[Iterable[CURIE]] = None,
        predicates: Optional[Iterable[PRED_CURIE]] = None,
        objects: Optional[Iterable[CURIE]] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
    ) -> Iterator[RELATIONSHIP]:
        subject_set = set(subjects) if subjects is not None else None
        predicate_set = set(predicates) if predicates is not None else None
        object_set = set(objects) if objects is not None else None
        for relationship in relationships:
            if relationship.scope == "tbox" and not include_tbox:
                continue
            if relationship.scope == "abox" and not include_abox:
                continue
            if subject_set is not None and relationship.subject not in subject_set:
                continue
            if predicate_set is not None and relationship.predicate not in predicate_set:
                continue
            if object_set is not None and relationship.object not in object_set:
                continue
            yield relationship.as_tuple()

    def relationships(
        self,
        subjects: Optional[Iterable[CURIE]] = None,
        predicates: Optional[Iterable[PRED_CURIE]] = None,
        objects: Optional[Iterable[CURIE]] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
        invert: bool = False,
    ) -> Iterator[RELATIONSHIP]:
        del exclude_blank
        if invert:
            for subject, predicate, object_curie in self.relationships(
                subjects=objects,
                predicates=predicates,
                objects=subjects,
                include_tbox=include_tbox,
                include_abox=include_abox,
                include_entailed=include_entailed,
            ):
                yield object_curie, predicate, subject
            return
        projected = (
            self._entailed_relationships() if include_entailed else self._direct_relationships()
        )
        yield from self._filter_relationships(
            projected,
            subjects=subjects,
            predicates=predicates,
            objects=objects,
            include_tbox=include_tbox,
            include_abox=include_abox,
        )

    def _all_relationships(self) -> Iterator[RELATIONSHIP]:
        for relationship in self._direct_relationships():
            yield relationship.as_tuple()

    def _all_entailed_relationships(self):
        for relationship in self._entailed_relationships():
            yield relationship.as_tuple()

    def _add_axiom(self, axiom: Component) -> None:
        if isinstance(axiom, AnnotatedComponent):
            self._ontology.add_axiom(axiom.component, set(axiom.ann))
        else:
            self._ontology.add_axiom(axiom)

    def set_axioms(self, axioms: List[Component]) -> None:
        for axiom in list(self._ontology.get_axioms()):
            self._ontology.remove_axiom(axiom.component)
        for axiom in axioms:
            self._add_axiom(axiom)
        self._invalidate_caches()

    def dump(self, path: Optional[str] = None, syntax: Optional[str] = None, **kwargs):
        syntax = syntax or "ofn"
        if syntax in NON_OWL_DUMP_SYNTAXES:
            # obograph-json, obo-format, fhir, cx, ... are produced by first
            # projecting the ontology to an OBO Graph
            DumperInterface.dump(self, path=path, syntax=syntax, **kwargs)
            return
        if syntax == "ofn":
            out = self._ontology.save_to_string("ofn")
        elif syntax in {"ttl", "turtle"}:
            rdfxml = self._ontology.save_to_string("owl")
            g = rdflib.Graph()
            g.parse(data=rdfxml, format="xml")
            out = g.serialize(format="ttl")
        elif syntax in {"owl", "owx"}:
            out = self._ontology.save_to_string(syntax)
        else:
            out = self._ontology.save_to_string(syntax)
        if path is None:
            print(out)
        elif isinstance(path, (str, Path)):
            Path(path).write_text(str(out), encoding="utf-8")
        else:
            path.write(str(out))

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: PatcherInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def _set_annotation_predicate_value(self, subject: CURIE, property: CURIE, value: Any):
        for axiom in list(self.annotation_assertion_axioms(subject, property)):
            self._ontology.remove_axiom(axiom)
        self._ontology.add_axiom(
            AnnotationAssertion(
                self.curie_to_entity_iri(subject),
                Annotation(
                    self.curie_to_annotation_property(property),
                    self._coerce_annotation_value(value),
                ),
            )
        )
        self._invalidate_caches()

    def apply_patch(
        self,
        patch: kgcl.Change,
        activity: kgcl.Activity = None,
        metadata: Optional[Mapping[PRED_CURIE, Any]] = None,
        configuration: kgcl.Configuration = None,
        strict=False,
    ) -> Optional[kgcl.Change]:
        if isinstance(patch, kgcl.NodeChange):
            about = patch.about_node
            if isinstance(patch, kgcl.NodeRename):
                self._set_annotation_predicate_value(about, LABEL_PREDICATE, patch.new_value)
            elif isinstance(patch, kgcl.NodeTextDefinitionChange):
                self._set_annotation_predicate_value(about, HAS_DEFINITION_CURIE, patch.new_value)
            elif isinstance(patch, kgcl.NewSynonym):
                self._ontology.add_axiom(
                    AnnotationAssertion(
                        self.curie_to_entity_iri(about),
                        Annotation(
                            self.curie_to_annotation_property(HAS_EXACT_SYNONYM),
                            self._coerce_annotation_value(patch.new_value),
                        ),
                    )
                )
                self._invalidate_caches()
            elif isinstance(patch, kgcl.NodeObsoletion):
                self._set_annotation_predicate_value(about, DEPRECATED_PREDICATE, value=True)
            elif isinstance(patch, kgcl.NodeDeletion):
                raise NotImplementedError("Deletions not supported yet")
            elif isinstance(patch, kgcl.NodeCreation):
                self._set_annotation_predicate_value(about, LABEL_PREDICATE, patch.name)
            elif isinstance(patch, kgcl.NameBecomesSynonym):
                label = self.label(about)
                self.apply_patch(
                    kgcl.NodeRename(id=f"{patch.id}-1", about_node=about, new_value=patch.new_value)
                )
                self.apply_patch(
                    kgcl.NewSynonym(id=f"{patch.id}-2", about_node=about, new_value=label)
                )
            else:
                raise NotImplementedError(f"Cannot handle patches of type {type(patch)}")
        elif isinstance(patch, kgcl.EdgeChange):
            subject = self.curie_to_class(patch.subject)
            object = self.curie_to_class(patch.object)
            if isinstance(patch, kgcl.EdgeCreation):
                if patch.predicate == IS_A or patch.predicate == "is_a":
                    self._ontology.add_axiom(SubClassOf(subject, object))
                else:
                    predicate = self.curie_to_object_property(patch.predicate)
                    self._ontology.add_axiom(
                        SubClassOf(subject, ObjectSomeValuesFrom(predicate, object))
                    )
                self._invalidate_caches()
            else:
                raise NotImplementedError(f"Cannot handle patches of type {type(patch)}")
        else:
            raise NotImplementedError(f"Cannot handle patches of type {type(patch)}")
        return patch
