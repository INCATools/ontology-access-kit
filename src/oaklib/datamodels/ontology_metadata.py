# Auto generated from ontology_metadata.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-05-29T22:52:46
# Schema: Ontology-Metadata
#
# id: http://purl.obolibrary.org/obo/omo/schema
# description: Schema for ontology metadata
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import as_dict
from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import URIRef

metamodel_version = "1.7.0"
version = "0.0.1"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
IAO = CurieNamespace("IAO", "http://purl.obolibrary.org/obo/IAO_")
NCIT = CurieNamespace("NCIT", "http://purl.obolibrary.org/obo/NCIT_")
OBI = CurieNamespace("OBI", "http://purl.obolibrary.org/obo/OBI_")
OIO = CurieNamespace("OIO", "http://www.geneontology.org/formats/oboInOwl#")
OMO = CurieNamespace("OMO", "http://purl.obolibrary.org/obo/OMO_")
RO = CurieNamespace("RO", "http://purl.obolibrary.org/obo/RO_")
BIOLINK = CurieNamespace("biolink", "https://w3id.org/biolink/vocab/")
DCTERMS = CurieNamespace("dcterms", "http://purl.org/dc/terms/")
FOAF = CurieNamespace("foaf", "http://xmlns.com/foaf/0.1/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OBO = CurieNamespace("obo", "http://purl.obolibrary.org/obo/")
OIO = CurieNamespace("oio", "http://www.geneontology.org/formats/oboInOwl#")
OMOSCHEMA = CurieNamespace("omoschema", "http://purl.obolibrary.org/obo/schema/")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
PROTEGE = CurieNamespace("protege", "http://example.org/UNKNOWN/protege/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov-o#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SDO = CurieNamespace("sdo", "http://schema.org/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = OMOSCHEMA


# Types
class IriType(Uriorcurie):
    """An IRI"""

    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "iri type"
    type_model_uri = OMOSCHEMA.IriType


class CURIELiteral(String):
    """A string representation of a CURIE"""

    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "CURIELiteral"
    type_model_uri = OMOSCHEMA.CURIELiteral


class URLLiteral(String):
    """A URL representation of a CURIE"""

    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "URLLiteral"
    type_model_uri = OMOSCHEMA.URLLiteral


class TidyString(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "tidy string"
    type_model_uri = OMOSCHEMA.TidyString


class LabelType(TidyString):
    """A string that provides a human-readable name for an entity"""

    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "label type"
    type_model_uri = OMOSCHEMA.LabelType


class NarrativeText(String):
    """A string that provides a human-readable description of something"""

    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "narrative text"
    type_model_uri = OMOSCHEMA.NarrativeText


# Class references
class NamedObjectId(URIorCURIE):
    pass


class OntologyId(NamedObjectId):
    pass


class TermId(NamedObjectId):
    pass


class ClassId(TermId):
    pass


class PropertyId(TermId):
    pass


class AnnotationPropertyId(PropertyId):
    pass


class ObjectPropertyId(PropertyId):
    pass


class TransitivePropertyId(ObjectPropertyId):
    pass


class NamedIndividualId(TermId):
    pass


class SubsetId(AnnotationPropertyId):
    pass


Any = Any


class AnnotationPropertyMixin(YAMLRoot):
    """
    Groups all annotation property bundles
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.AnnotationPropertyMixin
    class_class_curie: ClassVar[str] = "omoschema:AnnotationPropertyMixin"
    class_name: ClassVar[str] = "AnnotationPropertyMixin"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.AnnotationPropertyMixin


@dataclass
class HasMinimalMetadata(AnnotationPropertyMixin):
    """
    Absolute minimum metadata model
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.HasMinimalMetadata
    class_class_curie: ClassVar[str] = "omoschema:HasMinimalMetadata"
    class_name: ClassVar[str] = "HasMinimalMetadata"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.HasMinimalMetadata

    label: Optional[Union[str, LabelType]] = None
    definition: Optional[
        Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.label is not None and not isinstance(self.label, LabelType):
            self.label = LabelType(self.label)

        if not isinstance(self.definition, list):
            self.definition = [self.definition] if self.definition is not None else []
        self.definition = [
            v if isinstance(v, NarrativeText) else NarrativeText(v) for v in self.definition
        ]

        super().__post_init__(**kwargs)


@dataclass
class HasSynonyms(AnnotationPropertyMixin):
    """
    a mixin for a class whose members can have synonyms
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.HasSynonyms
    class_class_curie: ClassVar[str] = "omoschema:HasSynonyms"
    class_name: ClassVar[str] = "HasSynonyms"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.HasSynonyms

    has_exact_synonym: Optional[
        Union[Union[str, LabelType], List[Union[str, LabelType]]]
    ] = empty_list()
    has_narrow_synonym: Optional[
        Union[Union[str, LabelType], List[Union[str, LabelType]]]
    ] = empty_list()
    has_broad_synonym: Optional[
        Union[Union[str, LabelType], List[Union[str, LabelType]]]
    ] = empty_list()
    has_related_synonym: Optional[
        Union[Union[str, LabelType], List[Union[str, LabelType]]]
    ] = empty_list()
    alternative_term: Optional[Union[str, List[str]]] = empty_list()
    ISA_alternative_term: Optional[Union[str, List[str]]] = empty_list()
    IEDB_alternative_term: Optional[Union[str, List[str]]] = empty_list()
    editor_preferred_term: Optional[Union[str, List[str]]] = empty_list()
    OBO_foundry_unique_label: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_exact_synonym, list):
            self.has_exact_synonym = (
                [self.has_exact_synonym] if self.has_exact_synonym is not None else []
            )
        self.has_exact_synonym = [
            v if isinstance(v, LabelType) else LabelType(v) for v in self.has_exact_synonym
        ]

        if not isinstance(self.has_narrow_synonym, list):
            self.has_narrow_synonym = (
                [self.has_narrow_synonym] if self.has_narrow_synonym is not None else []
            )
        self.has_narrow_synonym = [
            v if isinstance(v, LabelType) else LabelType(v) for v in self.has_narrow_synonym
        ]

        if not isinstance(self.has_broad_synonym, list):
            self.has_broad_synonym = (
                [self.has_broad_synonym] if self.has_broad_synonym is not None else []
            )
        self.has_broad_synonym = [
            v if isinstance(v, LabelType) else LabelType(v) for v in self.has_broad_synonym
        ]

        if not isinstance(self.has_related_synonym, list):
            self.has_related_synonym = (
                [self.has_related_synonym] if self.has_related_synonym is not None else []
            )
        self.has_related_synonym = [
            v if isinstance(v, LabelType) else LabelType(v) for v in self.has_related_synonym
        ]

        if not isinstance(self.alternative_term, list):
            self.alternative_term = (
                [self.alternative_term] if self.alternative_term is not None else []
            )
        self.alternative_term = [v if isinstance(v, str) else str(v) for v in self.alternative_term]

        if not isinstance(self.ISA_alternative_term, list):
            self.ISA_alternative_term = (
                [self.ISA_alternative_term] if self.ISA_alternative_term is not None else []
            )
        self.ISA_alternative_term = [
            v if isinstance(v, str) else str(v) for v in self.ISA_alternative_term
        ]

        if not isinstance(self.IEDB_alternative_term, list):
            self.IEDB_alternative_term = (
                [self.IEDB_alternative_term] if self.IEDB_alternative_term is not None else []
            )
        self.IEDB_alternative_term = [
            v if isinstance(v, str) else str(v) for v in self.IEDB_alternative_term
        ]

        if not isinstance(self.editor_preferred_term, list):
            self.editor_preferred_term = (
                [self.editor_preferred_term] if self.editor_preferred_term is not None else []
            )
        self.editor_preferred_term = [
            v if isinstance(v, str) else str(v) for v in self.editor_preferred_term
        ]

        if not isinstance(self.OBO_foundry_unique_label, list):
            self.OBO_foundry_unique_label = (
                [self.OBO_foundry_unique_label] if self.OBO_foundry_unique_label is not None else []
            )
        self.OBO_foundry_unique_label = [
            v if isinstance(v, str) else str(v) for v in self.OBO_foundry_unique_label
        ]

        super().__post_init__(**kwargs)


@dataclass
class HasMappings(AnnotationPropertyMixin):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.HasMappings
    class_class_curie: ClassVar[str] = "omoschema:HasMappings"
    class_name: ClassVar[str] = "HasMappings"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.HasMappings

    broadMatch: Optional[Union[Union[dict, "Thing"], List[Union[dict, "Thing"]]]] = empty_list()
    closeMatch: Optional[Union[Union[dict, "Thing"], List[Union[dict, "Thing"]]]] = empty_list()
    exactMatch: Optional[Union[Union[dict, "Thing"], List[Union[dict, "Thing"]]]] = empty_list()
    narrowMatch: Optional[Union[Union[dict, "Thing"], List[Union[dict, "Thing"]]]] = empty_list()
    database_cross_reference: Optional[
        Union[Union[str, CURIELiteral], List[Union[str, CURIELiteral]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.broadMatch, list):
            self.broadMatch = [self.broadMatch] if self.broadMatch is not None else []
        self.broadMatch = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.broadMatch
        ]

        if not isinstance(self.closeMatch, list):
            self.closeMatch = [self.closeMatch] if self.closeMatch is not None else []
        self.closeMatch = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.closeMatch
        ]

        if not isinstance(self.exactMatch, list):
            self.exactMatch = [self.exactMatch] if self.exactMatch is not None else []
        self.exactMatch = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.exactMatch
        ]

        if not isinstance(self.narrowMatch, list):
            self.narrowMatch = [self.narrowMatch] if self.narrowMatch is not None else []
        self.narrowMatch = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.narrowMatch
        ]

        if not isinstance(self.database_cross_reference, list):
            self.database_cross_reference = (
                [self.database_cross_reference] if self.database_cross_reference is not None else []
            )
        self.database_cross_reference = [
            v if isinstance(v, CURIELiteral) else CURIELiteral(v)
            for v in self.database_cross_reference
        ]

        super().__post_init__(**kwargs)


@dataclass
class HasProvenance(AnnotationPropertyMixin):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.HasProvenance
    class_class_curie: ClassVar[str] = "omoschema:HasProvenance"
    class_name: ClassVar[str] = "HasProvenance"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.HasProvenance

    created_by: Optional[str] = None
    creation_date: Optional[Union[str, List[str]]] = empty_list()
    contributor: Optional[Union[Union[dict, "Thing"], List[Union[dict, "Thing"]]]] = empty_list()
    creator: Optional[Union[str, List[str]]] = empty_list()
    created: Optional[str] = None
    date: Optional[Union[str, List[str]]] = empty_list()
    isDefinedBy: Optional[Union[str, OntologyId]] = None
    editor_note: Optional[
        Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]
    ] = empty_list()
    term_editor: Optional[Union[str, List[str]]] = empty_list()
    definition_source: Optional[Union[str, List[str]]] = empty_list()
    ontology_term_requester: Optional[str] = None
    imported_from: Optional[
        Union[Union[str, NamedIndividualId], List[Union[str, NamedIndividualId]]]
    ] = empty_list()
    term_tracker_item: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.created_by is not None and not isinstance(self.created_by, str):
            self.created_by = str(self.created_by)

        if not isinstance(self.creation_date, list):
            self.creation_date = [self.creation_date] if self.creation_date is not None else []
        self.creation_date = [v if isinstance(v, str) else str(v) for v in self.creation_date]

        if not isinstance(self.contributor, list):
            self.contributor = [self.contributor] if self.contributor is not None else []
        self.contributor = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.contributor
        ]

        if not isinstance(self.creator, list):
            self.creator = [self.creator] if self.creator is not None else []
        self.creator = [v if isinstance(v, str) else str(v) for v in self.creator]

        if self.created is not None and not isinstance(self.created, str):
            self.created = str(self.created)

        if not isinstance(self.date, list):
            self.date = [self.date] if self.date is not None else []
        self.date = [v if isinstance(v, str) else str(v) for v in self.date]

        if self.isDefinedBy is not None and not isinstance(self.isDefinedBy, OntologyId):
            self.isDefinedBy = OntologyId(self.isDefinedBy)

        if not isinstance(self.editor_note, list):
            self.editor_note = [self.editor_note] if self.editor_note is not None else []
        self.editor_note = [
            v if isinstance(v, NarrativeText) else NarrativeText(v) for v in self.editor_note
        ]

        if not isinstance(self.term_editor, list):
            self.term_editor = [self.term_editor] if self.term_editor is not None else []
        self.term_editor = [v if isinstance(v, str) else str(v) for v in self.term_editor]

        if not isinstance(self.definition_source, list):
            self.definition_source = (
                [self.definition_source] if self.definition_source is not None else []
            )
        self.definition_source = [
            v if isinstance(v, str) else str(v) for v in self.definition_source
        ]

        if self.ontology_term_requester is not None and not isinstance(
            self.ontology_term_requester, str
        ):
            self.ontology_term_requester = str(self.ontology_term_requester)

        if not isinstance(self.imported_from, list):
            self.imported_from = [self.imported_from] if self.imported_from is not None else []
        self.imported_from = [
            v if isinstance(v, NamedIndividualId) else NamedIndividualId(v)
            for v in self.imported_from
        ]

        if not isinstance(self.term_tracker_item, list):
            self.term_tracker_item = (
                [self.term_tracker_item] if self.term_tracker_item is not None else []
            )
        self.term_tracker_item = [
            v if isinstance(v, str) else str(v) for v in self.term_tracker_item
        ]

        super().__post_init__(**kwargs)


@dataclass
class HasLifeCycle(AnnotationPropertyMixin):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.HasLifeCycle
    class_class_curie: ClassVar[str] = "omoschema:HasLifeCycle"
    class_name: ClassVar[str] = "HasLifeCycle"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.HasLifeCycle

    deprecated: Optional[Union[bool, Bool]] = None
    has_obsolescence_reason: Optional[str] = None
    term_replaced_by: Optional[Union[dict, Any]] = None
    consider: Optional[Union[Union[dict, Any], List[Union[dict, Any]]]] = empty_list()
    has_alternative_id: Optional[
        Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]
    ] = empty_list()
    excluded_from_QC_check: Optional[Union[dict, "Thing"]] = None
    excluded_subClassOf: Optional[
        Union[Union[str, ClassId], List[Union[str, ClassId]]]
    ] = empty_list()
    excluded_synonym: Optional[Union[str, List[str]]] = empty_list()
    should_conform_to: Optional[Union[dict, "Thing"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.deprecated is not None and not isinstance(self.deprecated, Bool):
            self.deprecated = Bool(self.deprecated)

        if self.has_obsolescence_reason is not None and not isinstance(
            self.has_obsolescence_reason, str
        ):
            self.has_obsolescence_reason = str(self.has_obsolescence_reason)

        if not isinstance(self.has_alternative_id, list):
            self.has_alternative_id = (
                [self.has_alternative_id] if self.has_alternative_id is not None else []
            )
        self.has_alternative_id = [
            v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.has_alternative_id
        ]

        if self.excluded_from_QC_check is not None and not isinstance(
            self.excluded_from_QC_check, Thing
        ):
            self.excluded_from_QC_check = Thing(**as_dict(self.excluded_from_QC_check))

        if not isinstance(self.excluded_subClassOf, list):
            self.excluded_subClassOf = (
                [self.excluded_subClassOf] if self.excluded_subClassOf is not None else []
            )
        self.excluded_subClassOf = [
            v if isinstance(v, ClassId) else ClassId(v) for v in self.excluded_subClassOf
        ]

        if not isinstance(self.excluded_synonym, list):
            self.excluded_synonym = (
                [self.excluded_synonym] if self.excluded_synonym is not None else []
            )
        self.excluded_synonym = [v if isinstance(v, str) else str(v) for v in self.excluded_synonym]

        if self.should_conform_to is not None and not isinstance(self.should_conform_to, Thing):
            self.should_conform_to = Thing(**as_dict(self.should_conform_to))

        super().__post_init__(**kwargs)


@dataclass
class HasCategory(AnnotationPropertyMixin):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.HasCategory
    class_class_curie: ClassVar[str] = "omoschema:HasCategory"
    class_name: ClassVar[str] = "HasCategory"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.HasCategory

    has_obo_namespace: Optional[Union[str, List[str]]] = empty_list()
    category: Optional[str] = None
    in_subset: Optional[Union[Union[str, SubsetId], List[Union[str, SubsetId]]]] = empty_list()
    conformsTo: Optional[Union[Union[dict, "Thing"], List[Union[dict, "Thing"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_obo_namespace, list):
            self.has_obo_namespace = (
                [self.has_obo_namespace] if self.has_obo_namespace is not None else []
            )
        self.has_obo_namespace = [
            v if isinstance(v, str) else str(v) for v in self.has_obo_namespace
        ]

        if self.category is not None and not isinstance(self.category, str):
            self.category = str(self.category)

        if not isinstance(self.in_subset, list):
            self.in_subset = [self.in_subset] if self.in_subset is not None else []
        self.in_subset = [v if isinstance(v, SubsetId) else SubsetId(v) for v in self.in_subset]

        if not isinstance(self.conformsTo, list):
            self.conformsTo = [self.conformsTo] if self.conformsTo is not None else []
        self.conformsTo = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.conformsTo
        ]

        super().__post_init__(**kwargs)


@dataclass
class HasUserInformation(AnnotationPropertyMixin):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.HasUserInformation
    class_class_curie: ClassVar[str] = "omoschema:HasUserInformation"
    class_name: ClassVar[str] = "HasUserInformation"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.HasUserInformation

    comment: Optional[Union[str, List[str]]] = empty_list()
    seeAlso: Optional[Union[Union[dict, "Thing"], List[Union[dict, "Thing"]]]] = empty_list()
    image: Optional[Union[dict, "Thing"]] = None
    example_of_usage: Optional[Union[str, List[str]]] = empty_list()
    curator_note: Optional[Union[str, List[str]]] = empty_list()
    has_curation_status: Optional[str] = None
    depicted_by: Optional[Union[str, List[str]]] = empty_list()
    page: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.comment, list):
            self.comment = [self.comment] if self.comment is not None else []
        self.comment = [v if isinstance(v, str) else str(v) for v in self.comment]

        if not isinstance(self.seeAlso, list):
            self.seeAlso = [self.seeAlso] if self.seeAlso is not None else []
        self.seeAlso = [v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.seeAlso]

        if self.image is not None and not isinstance(self.image, Thing):
            self.image = Thing(**as_dict(self.image))

        if not isinstance(self.example_of_usage, list):
            self.example_of_usage = (
                [self.example_of_usage] if self.example_of_usage is not None else []
            )
        self.example_of_usage = [v if isinstance(v, str) else str(v) for v in self.example_of_usage]

        if not isinstance(self.curator_note, list):
            self.curator_note = [self.curator_note] if self.curator_note is not None else []
        self.curator_note = [v if isinstance(v, str) else str(v) for v in self.curator_note]

        if self.has_curation_status is not None and not isinstance(self.has_curation_status, str):
            self.has_curation_status = str(self.has_curation_status)

        if not isinstance(self.depicted_by, list):
            self.depicted_by = [self.depicted_by] if self.depicted_by is not None else []
        self.depicted_by = [v if isinstance(v, str) else str(v) for v in self.depicted_by]

        if not isinstance(self.page, list):
            self.page = [self.page] if self.page is not None else []
        self.page = [v if isinstance(v, str) else str(v) for v in self.page]

        super().__post_init__(**kwargs)


@dataclass
class Thing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Thing
    class_class_curie: ClassVar[str] = "owl:Thing"
    class_name: ClassVar[str] = "Thing"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Thing

    type: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.type, list):
            self.type = [self.type] if self.type is not None else []
        self.type = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.type]

        super().__post_init__(**kwargs)


@dataclass
class NamedObject(Thing):
    """
    Anything with an IRI
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.NamedObject
    class_class_curie: ClassVar[str] = "omoschema:NamedObject"
    class_name: ClassVar[str] = "NamedObject"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.NamedObject

    id: Union[str, NamedObjectId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedObjectId):
            self.id = NamedObjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Ontology(NamedObject):
    """
    An OWL ontology
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Ontology
    class_class_curie: ClassVar[str] = "owl:Ontology"
    class_name: ClassVar[str] = "Ontology"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Ontology

    id: Union[str, OntologyId] = None
    title: Union[str, NarrativeText] = None
    license: Union[dict, Thing] = None
    versionIRI: Union[str, URIorCURIE] = None
    versionInfo: str = None
    has_ontology_root_term: Optional[
        Union[Union[str, ClassId], List[Union[str, ClassId]]]
    ] = empty_list()
    source: Optional[Union[str, List[str]]] = empty_list()
    comment: Optional[Union[str, List[str]]] = empty_list()
    creator: Optional[Union[str, List[str]]] = empty_list()
    created: Optional[str] = None
    imports: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OntologyId):
            self.id = OntologyId(self.id)

        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, NarrativeText):
            self.title = NarrativeText(self.title)

        if self._is_empty(self.license):
            self.MissingRequiredField("license")
        if not isinstance(self.license, Thing):
            self.license = Thing(**as_dict(self.license))

        if self._is_empty(self.versionIRI):
            self.MissingRequiredField("versionIRI")
        if not isinstance(self.versionIRI, URIorCURIE):
            self.versionIRI = URIorCURIE(self.versionIRI)

        if self._is_empty(self.versionInfo):
            self.MissingRequiredField("versionInfo")
        if not isinstance(self.versionInfo, str):
            self.versionInfo = str(self.versionInfo)

        if not isinstance(self.has_ontology_root_term, list):
            self.has_ontology_root_term = (
                [self.has_ontology_root_term] if self.has_ontology_root_term is not None else []
            )
        self.has_ontology_root_term = [
            v if isinstance(v, ClassId) else ClassId(v) for v in self.has_ontology_root_term
        ]

        if not isinstance(self.source, list):
            self.source = [self.source] if self.source is not None else []
        self.source = [v if isinstance(v, str) else str(v) for v in self.source]

        if not isinstance(self.comment, list):
            self.comment = [self.comment] if self.comment is not None else []
        self.comment = [v if isinstance(v, str) else str(v) for v in self.comment]

        if not isinstance(self.creator, list):
            self.creator = [self.creator] if self.creator is not None else []
        self.creator = [v if isinstance(v, str) else str(v) for v in self.creator]

        if self.created is not None and not isinstance(self.created, str):
            self.created = str(self.created)

        if self.imports is not None and not isinstance(self.imports, str):
            self.imports = str(self.imports)

        super().__post_init__(**kwargs)


@dataclass
class Term(NamedObject):
    """
    A NamedThing that includes classes, properties, but not ontologies
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.Term
    class_class_curie: ClassVar[str] = "omoschema:Term"
    class_name: ClassVar[str] = "Term"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Term

    id: Union[str, TermId] = None
    has_exact_synonym: Optional[
        Union[Union[str, LabelType], List[Union[str, LabelType]]]
    ] = empty_list()
    has_narrow_synonym: Optional[
        Union[Union[str, LabelType], List[Union[str, LabelType]]]
    ] = empty_list()
    has_broad_synonym: Optional[
        Union[Union[str, LabelType], List[Union[str, LabelType]]]
    ] = empty_list()
    has_related_synonym: Optional[
        Union[Union[str, LabelType], List[Union[str, LabelType]]]
    ] = empty_list()
    alternative_term: Optional[Union[str, List[str]]] = empty_list()
    ISA_alternative_term: Optional[Union[str, List[str]]] = empty_list()
    IEDB_alternative_term: Optional[Union[str, List[str]]] = empty_list()
    editor_preferred_term: Optional[Union[str, List[str]]] = empty_list()
    OBO_foundry_unique_label: Optional[Union[str, List[str]]] = empty_list()
    deprecated: Optional[Union[bool, Bool]] = None
    has_obsolescence_reason: Optional[str] = None
    term_replaced_by: Optional[Union[dict, Any]] = None
    consider: Optional[Union[Union[dict, Any], List[Union[dict, Any]]]] = empty_list()
    has_alternative_id: Optional[
        Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]
    ] = empty_list()
    excluded_from_QC_check: Optional[Union[dict, Thing]] = None
    excluded_subClassOf: Optional[
        Union[Union[str, ClassId], List[Union[str, ClassId]]]
    ] = empty_list()
    excluded_synonym: Optional[Union[str, List[str]]] = empty_list()
    should_conform_to: Optional[Union[dict, Thing]] = None
    created_by: Optional[str] = None
    creation_date: Optional[Union[str, List[str]]] = empty_list()
    contributor: Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]] = empty_list()
    creator: Optional[Union[str, List[str]]] = empty_list()
    created: Optional[str] = None
    date: Optional[Union[str, List[str]]] = empty_list()
    isDefinedBy: Optional[Union[str, OntologyId]] = None
    editor_note: Optional[
        Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]
    ] = empty_list()
    term_editor: Optional[Union[str, List[str]]] = empty_list()
    definition_source: Optional[Union[str, List[str]]] = empty_list()
    ontology_term_requester: Optional[str] = None
    imported_from: Optional[
        Union[Union[str, NamedIndividualId], List[Union[str, NamedIndividualId]]]
    ] = empty_list()
    term_tracker_item: Optional[Union[str, List[str]]] = empty_list()
    broadMatch: Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]] = empty_list()
    closeMatch: Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]] = empty_list()
    exactMatch: Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]] = empty_list()
    narrowMatch: Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]] = empty_list()
    database_cross_reference: Optional[
        Union[Union[str, CURIELiteral], List[Union[str, CURIELiteral]]]
    ] = empty_list()
    has_obo_namespace: Optional[Union[str, List[str]]] = empty_list()
    category: Optional[str] = None
    in_subset: Optional[Union[Union[str, SubsetId], List[Union[str, SubsetId]]]] = empty_list()
    conformsTo: Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]] = empty_list()
    comment: Optional[Union[str, List[str]]] = empty_list()
    seeAlso: Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]] = empty_list()
    image: Optional[Union[dict, Thing]] = None
    example_of_usage: Optional[Union[str, List[str]]] = empty_list()
    curator_note: Optional[Union[str, List[str]]] = empty_list()
    has_curation_status: Optional[str] = None
    depicted_by: Optional[Union[str, List[str]]] = empty_list()
    page: Optional[Union[str, List[str]]] = empty_list()
    label: Optional[Union[str, LabelType]] = None
    definition: Optional[
        Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_exact_synonym, list):
            self.has_exact_synonym = (
                [self.has_exact_synonym] if self.has_exact_synonym is not None else []
            )
        self.has_exact_synonym = [
            v if isinstance(v, LabelType) else LabelType(v) for v in self.has_exact_synonym
        ]

        if not isinstance(self.has_narrow_synonym, list):
            self.has_narrow_synonym = (
                [self.has_narrow_synonym] if self.has_narrow_synonym is not None else []
            )
        self.has_narrow_synonym = [
            v if isinstance(v, LabelType) else LabelType(v) for v in self.has_narrow_synonym
        ]

        if not isinstance(self.has_broad_synonym, list):
            self.has_broad_synonym = (
                [self.has_broad_synonym] if self.has_broad_synonym is not None else []
            )
        self.has_broad_synonym = [
            v if isinstance(v, LabelType) else LabelType(v) for v in self.has_broad_synonym
        ]

        if not isinstance(self.has_related_synonym, list):
            self.has_related_synonym = (
                [self.has_related_synonym] if self.has_related_synonym is not None else []
            )
        self.has_related_synonym = [
            v if isinstance(v, LabelType) else LabelType(v) for v in self.has_related_synonym
        ]

        if not isinstance(self.alternative_term, list):
            self.alternative_term = (
                [self.alternative_term] if self.alternative_term is not None else []
            )
        self.alternative_term = [v if isinstance(v, str) else str(v) for v in self.alternative_term]

        if not isinstance(self.ISA_alternative_term, list):
            self.ISA_alternative_term = (
                [self.ISA_alternative_term] if self.ISA_alternative_term is not None else []
            )
        self.ISA_alternative_term = [
            v if isinstance(v, str) else str(v) for v in self.ISA_alternative_term
        ]

        if not isinstance(self.IEDB_alternative_term, list):
            self.IEDB_alternative_term = (
                [self.IEDB_alternative_term] if self.IEDB_alternative_term is not None else []
            )
        self.IEDB_alternative_term = [
            v if isinstance(v, str) else str(v) for v in self.IEDB_alternative_term
        ]

        if not isinstance(self.editor_preferred_term, list):
            self.editor_preferred_term = (
                [self.editor_preferred_term] if self.editor_preferred_term is not None else []
            )
        self.editor_preferred_term = [
            v if isinstance(v, str) else str(v) for v in self.editor_preferred_term
        ]

        if not isinstance(self.OBO_foundry_unique_label, list):
            self.OBO_foundry_unique_label = (
                [self.OBO_foundry_unique_label] if self.OBO_foundry_unique_label is not None else []
            )
        self.OBO_foundry_unique_label = [
            v if isinstance(v, str) else str(v) for v in self.OBO_foundry_unique_label
        ]

        if self.deprecated is not None and not isinstance(self.deprecated, Bool):
            self.deprecated = Bool(self.deprecated)

        if self.has_obsolescence_reason is not None and not isinstance(
            self.has_obsolescence_reason, str
        ):
            self.has_obsolescence_reason = str(self.has_obsolescence_reason)

        if not isinstance(self.has_alternative_id, list):
            self.has_alternative_id = (
                [self.has_alternative_id] if self.has_alternative_id is not None else []
            )
        self.has_alternative_id = [
            v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.has_alternative_id
        ]

        if self.excluded_from_QC_check is not None and not isinstance(
            self.excluded_from_QC_check, Thing
        ):
            self.excluded_from_QC_check = Thing(**as_dict(self.excluded_from_QC_check))

        if not isinstance(self.excluded_subClassOf, list):
            self.excluded_subClassOf = (
                [self.excluded_subClassOf] if self.excluded_subClassOf is not None else []
            )
        self.excluded_subClassOf = [
            v if isinstance(v, ClassId) else ClassId(v) for v in self.excluded_subClassOf
        ]

        if not isinstance(self.excluded_synonym, list):
            self.excluded_synonym = (
                [self.excluded_synonym] if self.excluded_synonym is not None else []
            )
        self.excluded_synonym = [v if isinstance(v, str) else str(v) for v in self.excluded_synonym]

        if self.should_conform_to is not None and not isinstance(self.should_conform_to, Thing):
            self.should_conform_to = Thing(**as_dict(self.should_conform_to))

        if self.created_by is not None and not isinstance(self.created_by, str):
            self.created_by = str(self.created_by)

        if not isinstance(self.creation_date, list):
            self.creation_date = [self.creation_date] if self.creation_date is not None else []
        self.creation_date = [v if isinstance(v, str) else str(v) for v in self.creation_date]

        if not isinstance(self.contributor, list):
            self.contributor = [self.contributor] if self.contributor is not None else []
        self.contributor = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.contributor
        ]

        if not isinstance(self.creator, list):
            self.creator = [self.creator] if self.creator is not None else []
        self.creator = [v if isinstance(v, str) else str(v) for v in self.creator]

        if self.created is not None and not isinstance(self.created, str):
            self.created = str(self.created)

        if not isinstance(self.date, list):
            self.date = [self.date] if self.date is not None else []
        self.date = [v if isinstance(v, str) else str(v) for v in self.date]

        if self.isDefinedBy is not None and not isinstance(self.isDefinedBy, OntologyId):
            self.isDefinedBy = OntologyId(self.isDefinedBy)

        if not isinstance(self.editor_note, list):
            self.editor_note = [self.editor_note] if self.editor_note is not None else []
        self.editor_note = [
            v if isinstance(v, NarrativeText) else NarrativeText(v) for v in self.editor_note
        ]

        if not isinstance(self.term_editor, list):
            self.term_editor = [self.term_editor] if self.term_editor is not None else []
        self.term_editor = [v if isinstance(v, str) else str(v) for v in self.term_editor]

        if not isinstance(self.definition_source, list):
            self.definition_source = (
                [self.definition_source] if self.definition_source is not None else []
            )
        self.definition_source = [
            v if isinstance(v, str) else str(v) for v in self.definition_source
        ]

        if self.ontology_term_requester is not None and not isinstance(
            self.ontology_term_requester, str
        ):
            self.ontology_term_requester = str(self.ontology_term_requester)

        if not isinstance(self.imported_from, list):
            self.imported_from = [self.imported_from] if self.imported_from is not None else []
        self.imported_from = [
            v if isinstance(v, NamedIndividualId) else NamedIndividualId(v)
            for v in self.imported_from
        ]

        if not isinstance(self.term_tracker_item, list):
            self.term_tracker_item = (
                [self.term_tracker_item] if self.term_tracker_item is not None else []
            )
        self.term_tracker_item = [
            v if isinstance(v, str) else str(v) for v in self.term_tracker_item
        ]

        if not isinstance(self.broadMatch, list):
            self.broadMatch = [self.broadMatch] if self.broadMatch is not None else []
        self.broadMatch = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.broadMatch
        ]

        if not isinstance(self.closeMatch, list):
            self.closeMatch = [self.closeMatch] if self.closeMatch is not None else []
        self.closeMatch = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.closeMatch
        ]

        if not isinstance(self.exactMatch, list):
            self.exactMatch = [self.exactMatch] if self.exactMatch is not None else []
        self.exactMatch = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.exactMatch
        ]

        if not isinstance(self.narrowMatch, list):
            self.narrowMatch = [self.narrowMatch] if self.narrowMatch is not None else []
        self.narrowMatch = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.narrowMatch
        ]

        if not isinstance(self.database_cross_reference, list):
            self.database_cross_reference = (
                [self.database_cross_reference] if self.database_cross_reference is not None else []
            )
        self.database_cross_reference = [
            v if isinstance(v, CURIELiteral) else CURIELiteral(v)
            for v in self.database_cross_reference
        ]

        if not isinstance(self.has_obo_namespace, list):
            self.has_obo_namespace = (
                [self.has_obo_namespace] if self.has_obo_namespace is not None else []
            )
        self.has_obo_namespace = [
            v if isinstance(v, str) else str(v) for v in self.has_obo_namespace
        ]

        if self.category is not None and not isinstance(self.category, str):
            self.category = str(self.category)

        if not isinstance(self.in_subset, list):
            self.in_subset = [self.in_subset] if self.in_subset is not None else []
        self.in_subset = [v if isinstance(v, SubsetId) else SubsetId(v) for v in self.in_subset]

        if not isinstance(self.conformsTo, list):
            self.conformsTo = [self.conformsTo] if self.conformsTo is not None else []
        self.conformsTo = [
            v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.conformsTo
        ]

        if not isinstance(self.comment, list):
            self.comment = [self.comment] if self.comment is not None else []
        self.comment = [v if isinstance(v, str) else str(v) for v in self.comment]

        if not isinstance(self.seeAlso, list):
            self.seeAlso = [self.seeAlso] if self.seeAlso is not None else []
        self.seeAlso = [v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.seeAlso]

        if self.image is not None and not isinstance(self.image, Thing):
            self.image = Thing(**as_dict(self.image))

        if not isinstance(self.example_of_usage, list):
            self.example_of_usage = (
                [self.example_of_usage] if self.example_of_usage is not None else []
            )
        self.example_of_usage = [v if isinstance(v, str) else str(v) for v in self.example_of_usage]

        if not isinstance(self.curator_note, list):
            self.curator_note = [self.curator_note] if self.curator_note is not None else []
        self.curator_note = [v if isinstance(v, str) else str(v) for v in self.curator_note]

        if self.has_curation_status is not None and not isinstance(self.has_curation_status, str):
            self.has_curation_status = str(self.has_curation_status)

        if not isinstance(self.depicted_by, list):
            self.depicted_by = [self.depicted_by] if self.depicted_by is not None else []
        self.depicted_by = [v if isinstance(v, str) else str(v) for v in self.depicted_by]

        if not isinstance(self.page, list):
            self.page = [self.page] if self.page is not None else []
        self.page = [v if isinstance(v, str) else str(v) for v in self.page]

        if self.label is not None and not isinstance(self.label, LabelType):
            self.label = LabelType(self.label)

        if not isinstance(self.definition, list):
            self.definition = [self.definition] if self.definition is not None else []
        self.definition = [
            v if isinstance(v, NarrativeText) else NarrativeText(v) for v in self.definition
        ]

        super().__post_init__(**kwargs)


@dataclass
class Class(Term):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Class"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Class

    id: Union[str, ClassId] = None
    label: Union[str, LabelType] = None
    never_in_taxon: Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]] = empty_list()
    disconnected_from: Optional[Union[str, ClassId]] = None
    has_rank: Optional[Union[dict, Thing]] = None
    definition: Optional[
        Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]
    ] = empty_list()
    broadMatch: Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]] = empty_list()
    exactMatch: Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]] = empty_list()
    narrowMatch: Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]] = empty_list()
    closeMatch: Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]] = empty_list()
    subClassOf: Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]] = empty_list()
    disjointWith: Optional[Union[str, List[str]]] = empty_list()
    equivalentClass: Optional[
        Union[Union[dict, "ClassExpression"], List[Union[dict, "ClassExpression"]]]
    ] = empty_list()
    intersectionOf: Optional[Union[dict, "ClassExpression"]] = None
    cardinality: Optional[str] = None
    complementOf: Optional[str] = None
    oneOf: Optional[Union[dict, "ClassExpression"]] = None
    unionOf: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ClassId):
            self.id = ClassId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, LabelType):
            self.label = LabelType(self.label)

        if not isinstance(self.never_in_taxon, list):
            self.never_in_taxon = [self.never_in_taxon] if self.never_in_taxon is not None else []
        self.never_in_taxon = [
            v if isinstance(v, ClassId) else ClassId(v) for v in self.never_in_taxon
        ]

        if self.disconnected_from is not None and not isinstance(self.disconnected_from, ClassId):
            self.disconnected_from = ClassId(self.disconnected_from)

        if self.has_rank is not None and not isinstance(self.has_rank, Thing):
            self.has_rank = Thing(**as_dict(self.has_rank))

        if not isinstance(self.definition, list):
            self.definition = [self.definition] if self.definition is not None else []
        self.definition = [
            v if isinstance(v, NarrativeText) else NarrativeText(v) for v in self.definition
        ]

        if not isinstance(self.broadMatch, list):
            self.broadMatch = [self.broadMatch] if self.broadMatch is not None else []
        self.broadMatch = [v if isinstance(v, ClassId) else ClassId(v) for v in self.broadMatch]

        if not isinstance(self.exactMatch, list):
            self.exactMatch = [self.exactMatch] if self.exactMatch is not None else []
        self.exactMatch = [v if isinstance(v, ClassId) else ClassId(v) for v in self.exactMatch]

        if not isinstance(self.narrowMatch, list):
            self.narrowMatch = [self.narrowMatch] if self.narrowMatch is not None else []
        self.narrowMatch = [v if isinstance(v, ClassId) else ClassId(v) for v in self.narrowMatch]

        if not isinstance(self.closeMatch, list):
            self.closeMatch = [self.closeMatch] if self.closeMatch is not None else []
        self.closeMatch = [v if isinstance(v, ClassId) else ClassId(v) for v in self.closeMatch]

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, ClassId) else ClassId(v) for v in self.subClassOf]

        if not isinstance(self.disjointWith, list):
            self.disjointWith = [self.disjointWith] if self.disjointWith is not None else []
        self.disjointWith = [v if isinstance(v, str) else str(v) for v in self.disjointWith]

        if not isinstance(self.equivalentClass, list):
            self.equivalentClass = (
                [self.equivalentClass] if self.equivalentClass is not None else []
            )
        self.equivalentClass = [
            v if isinstance(v, ClassExpression) else ClassExpression(**as_dict(v))
            for v in self.equivalentClass
        ]

        if self.intersectionOf is not None and not isinstance(self.intersectionOf, ClassExpression):
            self.intersectionOf = ClassExpression(**as_dict(self.intersectionOf))

        if self.cardinality is not None and not isinstance(self.cardinality, str):
            self.cardinality = str(self.cardinality)

        if self.complementOf is not None and not isinstance(self.complementOf, str):
            self.complementOf = str(self.complementOf)

        if self.oneOf is not None and not isinstance(self.oneOf, ClassExpression):
            self.oneOf = ClassExpression(**as_dict(self.oneOf))

        if self.unionOf is not None and not isinstance(self.unionOf, str):
            self.unionOf = str(self.unionOf)

        super().__post_init__(**kwargs)


@dataclass
class Property(Term):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = RDF.Property
    class_class_curie: ClassVar[str] = "rdf:Property"
    class_name: ClassVar[str] = "Property"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Property

    id: Union[str, PropertyId] = None
    domain: Optional[Union[str, List[str]]] = empty_list()
    range: Optional[Union[str, List[str]]] = empty_list()
    is_class_level: Optional[Union[bool, Bool]] = None
    is_metadata_tag: Optional[Union[bool, Bool]] = None
    label: Optional[Union[str, LabelType]] = None
    definition: Optional[
        Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]
    ] = empty_list()
    broadMatch: Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]] = empty_list()
    exactMatch: Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]] = empty_list()
    narrowMatch: Optional[
        Union[Union[str, PropertyId], List[Union[str, PropertyId]]]
    ] = empty_list()
    closeMatch: Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]] = empty_list()
    subClassOf: Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.domain, list):
            self.domain = [self.domain] if self.domain is not None else []
        self.domain = [v if isinstance(v, str) else str(v) for v in self.domain]

        if not isinstance(self.range, list):
            self.range = [self.range] if self.range is not None else []
        self.range = [v if isinstance(v, str) else str(v) for v in self.range]

        if self.is_class_level is not None and not isinstance(self.is_class_level, Bool):
            self.is_class_level = Bool(self.is_class_level)

        if self.is_metadata_tag is not None and not isinstance(self.is_metadata_tag, Bool):
            self.is_metadata_tag = Bool(self.is_metadata_tag)

        if self.label is not None and not isinstance(self.label, LabelType):
            self.label = LabelType(self.label)

        if not isinstance(self.definition, list):
            self.definition = [self.definition] if self.definition is not None else []
        self.definition = [
            v if isinstance(v, NarrativeText) else NarrativeText(v) for v in self.definition
        ]

        if not isinstance(self.broadMatch, list):
            self.broadMatch = [self.broadMatch] if self.broadMatch is not None else []
        self.broadMatch = [
            v if isinstance(v, PropertyId) else PropertyId(v) for v in self.broadMatch
        ]

        if not isinstance(self.exactMatch, list):
            self.exactMatch = [self.exactMatch] if self.exactMatch is not None else []
        self.exactMatch = [
            v if isinstance(v, PropertyId) else PropertyId(v) for v in self.exactMatch
        ]

        if not isinstance(self.narrowMatch, list):
            self.narrowMatch = [self.narrowMatch] if self.narrowMatch is not None else []
        self.narrowMatch = [
            v if isinstance(v, PropertyId) else PropertyId(v) for v in self.narrowMatch
        ]

        if not isinstance(self.closeMatch, list):
            self.closeMatch = [self.closeMatch] if self.closeMatch is not None else []
        self.closeMatch = [
            v if isinstance(v, PropertyId) else PropertyId(v) for v in self.closeMatch
        ]

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [
            v if isinstance(v, PropertyId) else PropertyId(v) for v in self.subClassOf
        ]

        super().__post_init__(**kwargs)


@dataclass
class AnnotationProperty(Property):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.AnnotationProperty
    class_class_curie: ClassVar[str] = "owl:AnnotationProperty"
    class_name: ClassVar[str] = "AnnotationProperty"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.AnnotationProperty

    id: Union[str, AnnotationPropertyId] = None
    shorthand: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnnotationPropertyId):
            self.id = AnnotationPropertyId(self.id)

        if not isinstance(self.shorthand, list):
            self.shorthand = [self.shorthand] if self.shorthand is not None else []
        self.shorthand = [v if isinstance(v, str) else str(v) for v in self.shorthand]

        super().__post_init__(**kwargs)


@dataclass
class ObjectProperty(Property):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.ObjectProperty
    class_class_curie: ClassVar[str] = "owl:ObjectProperty"
    class_name: ClassVar[str] = "ObjectProperty"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.ObjectProperty

    id: Union[str, ObjectPropertyId] = None
    temporal_interpretation: Optional[Union[str, NamedIndividualId]] = None
    is_cyclic: Optional[Union[bool, Bool]] = None
    is_transitive: Optional[Union[bool, Bool]] = None
    shorthand: Optional[Union[str, List[str]]] = empty_list()
    equivalentProperty: Optional[
        Union[Union[str, PropertyId], List[Union[str, PropertyId]]]
    ] = empty_list()
    inverseOf: Optional[Union[str, PropertyId]] = None
    propertyChainAxiom: Optional[Union[str, List[str]]] = empty_list()
    disjointWith: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ObjectPropertyId):
            self.id = ObjectPropertyId(self.id)

        if self.temporal_interpretation is not None and not isinstance(
            self.temporal_interpretation, NamedIndividualId
        ):
            self.temporal_interpretation = NamedIndividualId(self.temporal_interpretation)

        if self.is_cyclic is not None and not isinstance(self.is_cyclic, Bool):
            self.is_cyclic = Bool(self.is_cyclic)

        if self.is_transitive is not None and not isinstance(self.is_transitive, Bool):
            self.is_transitive = Bool(self.is_transitive)

        if not isinstance(self.shorthand, list):
            self.shorthand = [self.shorthand] if self.shorthand is not None else []
        self.shorthand = [v if isinstance(v, str) else str(v) for v in self.shorthand]

        if not isinstance(self.equivalentProperty, list):
            self.equivalentProperty = (
                [self.equivalentProperty] if self.equivalentProperty is not None else []
            )
        self.equivalentProperty = [
            v if isinstance(v, PropertyId) else PropertyId(v) for v in self.equivalentProperty
        ]

        if self.inverseOf is not None and not isinstance(self.inverseOf, PropertyId):
            self.inverseOf = PropertyId(self.inverseOf)

        if not isinstance(self.propertyChainAxiom, list):
            self.propertyChainAxiom = (
                [self.propertyChainAxiom] if self.propertyChainAxiom is not None else []
            )
        self.propertyChainAxiom = [
            v if isinstance(v, str) else str(v) for v in self.propertyChainAxiom
        ]

        if not isinstance(self.disjointWith, list):
            self.disjointWith = [self.disjointWith] if self.disjointWith is not None else []
        self.disjointWith = [v if isinstance(v, str) else str(v) for v in self.disjointWith]

        super().__post_init__(**kwargs)


@dataclass
class TransitiveProperty(ObjectProperty):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.TransitiveProperty
    class_class_curie: ClassVar[str] = "omoschema:TransitiveProperty"
    class_name: ClassVar[str] = "TransitiveProperty"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.TransitiveProperty

    id: Union[str, TransitivePropertyId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TransitivePropertyId):
            self.id = TransitivePropertyId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class NamedIndividual(Term):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.NamedIndividual
    class_class_curie: ClassVar[str] = "owl:NamedIndividual"
    class_name: ClassVar[str] = "NamedIndividual"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.NamedIndividual

    id: Union[str, NamedIndividualId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedIndividualId):
            self.id = NamedIndividualId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Annotation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.Annotation
    class_class_curie: ClassVar[str] = "omoschema:Annotation"
    class_name: ClassVar[str] = "Annotation"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Annotation

    predicate: Optional[str] = None
    object: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.predicate is not None and not isinstance(self.predicate, str):
            self.predicate = str(self.predicate)

        if self.object is not None and not isinstance(self.object, str):
            self.object = str(self.object)

        super().__post_init__(**kwargs)


@dataclass
class Axiom(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Axiom
    class_class_curie: ClassVar[str] = "owl:Axiom"
    class_name: ClassVar[str] = "Axiom"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Axiom

    annotatedProperty: Optional[Union[str, AnnotationPropertyId]] = None
    annotatedSource: Optional[Union[str, NamedObjectId]] = None
    annotatedTarget: Optional[Union[dict, Any]] = None
    annotations: Optional[
        Union[Union[dict, Annotation], List[Union[dict, Annotation]]]
    ] = empty_list()
    source: Optional[Union[str, List[str]]] = empty_list()
    is_inferred: Optional[Union[bool, Bool]] = None
    notes: Optional[Union[str, List[str]]] = empty_list()
    url: Optional[str] = None
    has_axiom_label: Optional[Union[dict, Thing]] = None
    is_a_defining_property_chain_axiom: Optional[str] = None
    is_a_defining_property_chain_axiom_where_second_argument_is_reflexive: Optional[str] = None
    created_by: Optional[str] = None
    date_retrieved: Optional[str] = None
    evidence: Optional[str] = None
    external_ontology: Optional[Union[str, List[str]]] = empty_list()
    database_cross_reference: Optional[
        Union[Union[str, CURIELiteral], List[Union[str, CURIELiteral]]]
    ] = empty_list()
    has_exact_synonym: Optional[
        Union[Union[str, LabelType], List[Union[str, LabelType]]]
    ] = empty_list()
    has_synonym_type: Optional[
        Union[Union[str, AnnotationPropertyId], List[Union[str, AnnotationPropertyId]]]
    ] = empty_list()
    comment: Optional[Union[str, List[str]]] = empty_list()
    label: Optional[Union[str, LabelType]] = None
    seeAlso: Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.annotatedProperty is not None and not isinstance(
            self.annotatedProperty, AnnotationPropertyId
        ):
            self.annotatedProperty = AnnotationPropertyId(self.annotatedProperty)

        if self.annotatedSource is not None and not isinstance(self.annotatedSource, NamedObjectId):
            self.annotatedSource = NamedObjectId(self.annotatedSource)

        if not isinstance(self.annotations, list):
            self.annotations = [self.annotations] if self.annotations is not None else []
        self.annotations = [
            v if isinstance(v, Annotation) else Annotation(**as_dict(v)) for v in self.annotations
        ]

        if not isinstance(self.source, list):
            self.source = [self.source] if self.source is not None else []
        self.source = [v if isinstance(v, str) else str(v) for v in self.source]

        if self.is_inferred is not None and not isinstance(self.is_inferred, Bool):
            self.is_inferred = Bool(self.is_inferred)

        if not isinstance(self.notes, list):
            self.notes = [self.notes] if self.notes is not None else []
        self.notes = [v if isinstance(v, str) else str(v) for v in self.notes]

        if self.url is not None and not isinstance(self.url, str):
            self.url = str(self.url)

        if self.has_axiom_label is not None and not isinstance(self.has_axiom_label, Thing):
            self.has_axiom_label = Thing(**as_dict(self.has_axiom_label))

        if self.is_a_defining_property_chain_axiom is not None and not isinstance(
            self.is_a_defining_property_chain_axiom, str
        ):
            self.is_a_defining_property_chain_axiom = str(self.is_a_defining_property_chain_axiom)

        if (
            self.is_a_defining_property_chain_axiom_where_second_argument_is_reflexive is not None
            and not isinstance(
                self.is_a_defining_property_chain_axiom_where_second_argument_is_reflexive, str
            )
        ):
            self.is_a_defining_property_chain_axiom_where_second_argument_is_reflexive = str(
                self.is_a_defining_property_chain_axiom_where_second_argument_is_reflexive
            )

        if self.created_by is not None and not isinstance(self.created_by, str):
            self.created_by = str(self.created_by)

        if self.date_retrieved is not None and not isinstance(self.date_retrieved, str):
            self.date_retrieved = str(self.date_retrieved)

        if self.evidence is not None and not isinstance(self.evidence, str):
            self.evidence = str(self.evidence)

        if not isinstance(self.external_ontology, list):
            self.external_ontology = (
                [self.external_ontology] if self.external_ontology is not None else []
            )
        self.external_ontology = [
            v if isinstance(v, str) else str(v) for v in self.external_ontology
        ]

        if not isinstance(self.database_cross_reference, list):
            self.database_cross_reference = (
                [self.database_cross_reference] if self.database_cross_reference is not None else []
            )
        self.database_cross_reference = [
            v if isinstance(v, CURIELiteral) else CURIELiteral(v)
            for v in self.database_cross_reference
        ]

        if not isinstance(self.has_exact_synonym, list):
            self.has_exact_synonym = (
                [self.has_exact_synonym] if self.has_exact_synonym is not None else []
            )
        self.has_exact_synonym = [
            v if isinstance(v, LabelType) else LabelType(v) for v in self.has_exact_synonym
        ]

        if not isinstance(self.has_synonym_type, list):
            self.has_synonym_type = (
                [self.has_synonym_type] if self.has_synonym_type is not None else []
            )
        self.has_synonym_type = [
            v if isinstance(v, AnnotationPropertyId) else AnnotationPropertyId(v)
            for v in self.has_synonym_type
        ]

        if not isinstance(self.comment, list):
            self.comment = [self.comment] if self.comment is not None else []
        self.comment = [v if isinstance(v, str) else str(v) for v in self.comment]

        if self.label is not None and not isinstance(self.label, LabelType):
            self.label = LabelType(self.label)

        if not isinstance(self.seeAlso, list):
            self.seeAlso = [self.seeAlso] if self.seeAlso is not None else []
        self.seeAlso = [v if isinstance(v, Thing) else Thing(**as_dict(v)) for v in self.seeAlso]

        super().__post_init__(**kwargs)


@dataclass
class Subset(AnnotationProperty):
    """
    A collection of terms grouped for some purpose
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OIO.Subset
    class_class_curie: ClassVar[str] = "oio:Subset"
    class_name: ClassVar[str] = "Subset"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Subset

    id: Union[str, SubsetId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SubsetId):
            self.id = SubsetId(self.id)

        super().__post_init__(**kwargs)


class Anonymous(YAMLRoot):
    """
    Abstract root class for all anonymous (non-named; lacking an identifier) expressions
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.Anonymous
    class_class_curie: ClassVar[str] = "omoschema:Anonymous"
    class_name: ClassVar[str] = "Anonymous"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Anonymous


class AnonymousClassExpression(Anonymous):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.AnonymousClassExpression
    class_class_curie: ClassVar[str] = "omoschema:AnonymousClassExpression"
    class_name: ClassVar[str] = "AnonymousClassExpression"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.AnonymousClassExpression


@dataclass
class Restriction(AnonymousClassExpression):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Restriction
    class_class_curie: ClassVar[str] = "owl:Restriction"
    class_name: ClassVar[str] = "Restriction"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Restriction

    onProperty: Optional[
        Union[Union[dict, "PropertyExpression"], List[Union[dict, "PropertyExpression"]]]
    ] = empty_list()
    someValuesFrom: Optional[Union[str, List[str]]] = empty_list()
    allValuesFrom: Optional[str] = None
    disjointWith: Optional[Union[str, List[str]]] = empty_list()
    equivalentClass: Optional[
        Union[Union[dict, "ClassExpression"], List[Union[dict, "ClassExpression"]]]
    ] = empty_list()
    intersectionOf: Optional[Union[dict, "ClassExpression"]] = None
    subClassOf: Optional[
        Union[Union[dict, "ClassExpression"], List[Union[dict, "ClassExpression"]]]
    ] = empty_list()
    cardinality: Optional[str] = None
    complementOf: Optional[str] = None
    oneOf: Optional[Union[dict, "ClassExpression"]] = None
    unionOf: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.onProperty, list):
            self.onProperty = [self.onProperty] if self.onProperty is not None else []
        self.onProperty = [
            v if isinstance(v, PropertyExpression) else PropertyExpression(**as_dict(v))
            for v in self.onProperty
        ]

        if not isinstance(self.someValuesFrom, list):
            self.someValuesFrom = [self.someValuesFrom] if self.someValuesFrom is not None else []
        self.someValuesFrom = [v if isinstance(v, str) else str(v) for v in self.someValuesFrom]

        if self.allValuesFrom is not None and not isinstance(self.allValuesFrom, str):
            self.allValuesFrom = str(self.allValuesFrom)

        if not isinstance(self.disjointWith, list):
            self.disjointWith = [self.disjointWith] if self.disjointWith is not None else []
        self.disjointWith = [v if isinstance(v, str) else str(v) for v in self.disjointWith]

        if not isinstance(self.equivalentClass, list):
            self.equivalentClass = (
                [self.equivalentClass] if self.equivalentClass is not None else []
            )
        self.equivalentClass = [
            v if isinstance(v, ClassExpression) else ClassExpression(**as_dict(v))
            for v in self.equivalentClass
        ]

        if self.intersectionOf is not None and not isinstance(self.intersectionOf, ClassExpression):
            self.intersectionOf = ClassExpression(**as_dict(self.intersectionOf))

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [
            v if isinstance(v, ClassExpression) else ClassExpression(**as_dict(v))
            for v in self.subClassOf
        ]

        if self.cardinality is not None and not isinstance(self.cardinality, str):
            self.cardinality = str(self.cardinality)

        if self.complementOf is not None and not isinstance(self.complementOf, str):
            self.complementOf = str(self.complementOf)

        if self.oneOf is not None and not isinstance(self.oneOf, ClassExpression):
            self.oneOf = ClassExpression(**as_dict(self.oneOf))

        if self.unionOf is not None and not isinstance(self.unionOf, str):
            self.unionOf = str(self.unionOf)

        super().__post_init__(**kwargs)


class Expression(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.Expression
    class_class_curie: ClassVar[str] = "omoschema:Expression"
    class_name: ClassVar[str] = "Expression"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.Expression


@dataclass
class ClassExpression(Expression):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.ClassExpression
    class_class_curie: ClassVar[str] = "omoschema:ClassExpression"
    class_name: ClassVar[str] = "ClassExpression"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.ClassExpression

    disjointWith: Optional[Union[str, List[str]]] = empty_list()
    equivalentClass: Optional[
        Union[Union[dict, "ClassExpression"], List[Union[dict, "ClassExpression"]]]
    ] = empty_list()
    intersectionOf: Optional[Union[dict, "ClassExpression"]] = None
    subClassOf: Optional[
        Union[Union[dict, "ClassExpression"], List[Union[dict, "ClassExpression"]]]
    ] = empty_list()
    cardinality: Optional[str] = None
    complementOf: Optional[str] = None
    oneOf: Optional[Union[dict, "ClassExpression"]] = None
    unionOf: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.disjointWith, list):
            self.disjointWith = [self.disjointWith] if self.disjointWith is not None else []
        self.disjointWith = [v if isinstance(v, str) else str(v) for v in self.disjointWith]

        if not isinstance(self.equivalentClass, list):
            self.equivalentClass = (
                [self.equivalentClass] if self.equivalentClass is not None else []
            )
        self.equivalentClass = [
            v if isinstance(v, ClassExpression) else ClassExpression(**as_dict(v))
            for v in self.equivalentClass
        ]

        if self.intersectionOf is not None and not isinstance(self.intersectionOf, ClassExpression):
            self.intersectionOf = ClassExpression(**as_dict(self.intersectionOf))

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [
            v if isinstance(v, ClassExpression) else ClassExpression(**as_dict(v))
            for v in self.subClassOf
        ]

        if self.cardinality is not None and not isinstance(self.cardinality, str):
            self.cardinality = str(self.cardinality)

        if self.complementOf is not None and not isinstance(self.complementOf, str):
            self.complementOf = str(self.complementOf)

        if self.oneOf is not None and not isinstance(self.oneOf, ClassExpression):
            self.oneOf = ClassExpression(**as_dict(self.oneOf))

        if self.unionOf is not None and not isinstance(self.unionOf, str):
            self.unionOf = str(self.unionOf)

        super().__post_init__(**kwargs)


@dataclass
class PropertyExpression(Expression):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.PropertyExpression
    class_class_curie: ClassVar[str] = "omoschema:PropertyExpression"
    class_name: ClassVar[str] = "PropertyExpression"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.PropertyExpression

    disjointWith: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.disjointWith, list):
            self.disjointWith = [self.disjointWith] if self.disjointWith is not None else []
        self.disjointWith = [v if isinstance(v, str) else str(v) for v in self.disjointWith]

        super().__post_init__(**kwargs)


@dataclass
class ObsoleteAspect(YAMLRoot):
    """
    Auto-classifies anything that is obsolete
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.ObsoleteAspect
    class_class_curie: ClassVar[str] = "omoschema:ObsoleteAspect"
    class_name: ClassVar[str] = "ObsoleteAspect"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.ObsoleteAspect

    label: Optional[Union[str, LabelType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.label is not None and not isinstance(self.label, LabelType):
            self.label = LabelType(self.label)

        super().__post_init__(**kwargs)


class NotObsoleteAspect(YAMLRoot):
    """
    Auto-classifies anything that is not obsolete
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OMOSCHEMA.NotObsoleteAspect
    class_class_curie: ClassVar[str] = "omoschema:NotObsoleteAspect"
    class_name: ClassVar[str] = "NotObsoleteAspect"
    class_model_uri: ClassVar[URIRef] = OMOSCHEMA.NotObsoleteAspect


# Enumerations


# Slots
class slots:
    pass


slots.core_property = Slot(
    uri=OMOSCHEMA.core_property,
    name="core_property",
    curie=OMOSCHEMA.curie("core_property"),
    model_uri=OMOSCHEMA.core_property,
    domain=None,
    range=Optional[str],
)

slots.id = Slot(
    uri=OMOSCHEMA.id,
    name="id",
    curie=OMOSCHEMA.curie("id"),
    model_uri=OMOSCHEMA.id,
    domain=None,
    range=URIRef,
)

slots.label = Slot(
    uri=RDFS.label,
    name="label",
    curie=RDFS.curie("label"),
    model_uri=OMOSCHEMA.label,
    domain=None,
    range=Optional[Union[str, LabelType]],
)

slots.annotations = Slot(
    uri=OMOSCHEMA.annotations,
    name="annotations",
    curie=OMOSCHEMA.curie("annotations"),
    model_uri=OMOSCHEMA.annotations,
    domain=None,
    range=Optional[Union[Union[dict, Annotation], List[Union[dict, Annotation]]]],
)

slots.definition = Slot(
    uri=IAO["0000115"],
    name="definition",
    curie=IAO.curie("0000115"),
    model_uri=OMOSCHEMA.definition,
    domain=None,
    range=Optional[Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]],
)

slots.title = Slot(
    uri=DCTERMS.title,
    name="title",
    curie=DCTERMS.curie("title"),
    model_uri=OMOSCHEMA.title,
    domain=None,
    range=Optional[Union[str, NarrativeText]],
)

slots.match_aspect = Slot(
    uri=OMOSCHEMA.match_aspect,
    name="match_aspect",
    curie=OMOSCHEMA.curie("match_aspect"),
    model_uri=OMOSCHEMA.match_aspect,
    domain=None,
    range=Optional[str],
)

slots.match = Slot(
    uri=OMOSCHEMA.match,
    name="match",
    curie=OMOSCHEMA.curie("match"),
    model_uri=OMOSCHEMA.match,
    domain=None,
    range=Optional[str],
)

slots.broadMatch = Slot(
    uri=SKOS.broadMatch,
    name="broadMatch",
    curie=SKOS.curie("broadMatch"),
    model_uri=OMOSCHEMA.broadMatch,
    domain=None,
    range=Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]],
)

slots.closeMatch = Slot(
    uri=SKOS.closeMatch,
    name="closeMatch",
    curie=SKOS.curie("closeMatch"),
    model_uri=OMOSCHEMA.closeMatch,
    domain=None,
    range=Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]],
)

slots.exactMatch = Slot(
    uri=SKOS.exactMatch,
    name="exactMatch",
    curie=SKOS.curie("exactMatch"),
    model_uri=OMOSCHEMA.exactMatch,
    domain=None,
    range=Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]],
)

slots.narrowMatch = Slot(
    uri=SKOS.narrowMatch,
    name="narrowMatch",
    curie=SKOS.curie("narrowMatch"),
    model_uri=OMOSCHEMA.narrowMatch,
    domain=None,
    range=Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]],
)

slots.database_cross_reference = Slot(
    uri=OIO.hasDbXref,
    name="database_cross_reference",
    curie=OIO.curie("hasDbXref"),
    model_uri=OMOSCHEMA.database_cross_reference,
    domain=None,
    range=Optional[Union[Union[str, CURIELiteral], List[Union[str, CURIELiteral]]]],
)

slots.informative_property = Slot(
    uri=OMOSCHEMA.informative_property,
    name="informative_property",
    curie=OMOSCHEMA.curie("informative_property"),
    model_uri=OMOSCHEMA.informative_property,
    domain=None,
    range=Optional[str],
)

slots.comment = Slot(
    uri=RDFS.comment,
    name="comment",
    curie=RDFS.curie("comment"),
    model_uri=OMOSCHEMA.comment,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.category = Slot(
    uri=BIOLINK.category,
    name="category",
    curie=BIOLINK.curie("category"),
    model_uri=OMOSCHEMA.category,
    domain=None,
    range=Optional[str],
)

slots.image = Slot(
    uri=SDO.image,
    name="image",
    curie=SDO.curie("image"),
    model_uri=OMOSCHEMA.image,
    domain=None,
    range=Optional[Union[dict, Thing]],
)

slots.example_of_usage = Slot(
    uri=IAO["0000112"],
    name="example_of_usage",
    curie=IAO.curie("0000112"),
    model_uri=OMOSCHEMA.example_of_usage,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.changeNote = Slot(
    uri=SKOS.changeNote,
    name="changeNote",
    curie=SKOS.curie("changeNote"),
    model_uri=OMOSCHEMA.changeNote,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.has_curation_status = Slot(
    uri=IAO["0000114"],
    name="has_curation_status",
    curie=IAO.curie("0000114"),
    model_uri=OMOSCHEMA.has_curation_status,
    domain=None,
    range=Optional[str],
)

slots.defaultLanguage = Slot(
    uri=PROTEGE.defaultLanguage,
    name="defaultLanguage",
    curie=PROTEGE.curie("defaultLanguage"),
    model_uri=OMOSCHEMA.defaultLanguage,
    domain=None,
    range=Optional[str],
)

slots.has_ontology_root_term = Slot(
    uri=IAO["0000700"],
    name="has_ontology_root_term",
    curie=IAO.curie("0000700"),
    model_uri=OMOSCHEMA.has_ontology_root_term,
    domain=None,
    range=Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]],
)

slots.conformsTo = Slot(
    uri=DCTERMS.conformsTo,
    name="conformsTo",
    curie=DCTERMS.curie("conformsTo"),
    model_uri=OMOSCHEMA.conformsTo,
    domain=None,
    range=Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]],
)

slots.license = Slot(
    uri=DCTERMS.license,
    name="license",
    curie=DCTERMS.curie("license"),
    model_uri=OMOSCHEMA.license,
    domain=None,
    range=Optional[Union[dict, Thing]],
)

slots.depicted_by = Slot(
    uri=FOAF.depicted_by,
    name="depicted_by",
    curie=FOAF.curie("depicted_by"),
    model_uri=OMOSCHEMA.depicted_by,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.page = Slot(
    uri=FOAF.page,
    name="page",
    curie=FOAF.curie("page"),
    model_uri=OMOSCHEMA.page,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.version_property = Slot(
    uri=OMOSCHEMA.version_property,
    name="version_property",
    curie=OMOSCHEMA.curie("version_property"),
    model_uri=OMOSCHEMA.version_property,
    domain=None,
    range=Optional[str],
)

slots.versionIRI = Slot(
    uri=OWL.versionIRI,
    name="versionIRI",
    curie=OWL.curie("versionIRI"),
    model_uri=OMOSCHEMA.versionIRI,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.versionInfo = Slot(
    uri=OWL.versionInfo,
    name="versionInfo",
    curie=OWL.curie("versionInfo"),
    model_uri=OMOSCHEMA.versionInfo,
    domain=None,
    range=Optional[str],
)

slots.obsoletion_related_property = Slot(
    uri=OMOSCHEMA.obsoletion_related_property,
    name="obsoletion_related_property",
    curie=OMOSCHEMA.curie("obsoletion_related_property"),
    model_uri=OMOSCHEMA.obsoletion_related_property,
    domain=None,
    range=Optional[str],
)

slots.deprecated = Slot(
    uri=OWL.deprecated,
    name="deprecated",
    curie=OWL.curie("deprecated"),
    model_uri=OMOSCHEMA.deprecated,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.term_replaced_by = Slot(
    uri=IAO["0100001"],
    name="term_replaced_by",
    curie=IAO.curie("0100001"),
    model_uri=OMOSCHEMA.term_replaced_by,
    domain=None,
    range=Optional[Union[dict, Any]],
)

slots.has_obsolescence_reason = Slot(
    uri=IAO["0000231"],
    name="has_obsolescence_reason",
    curie=IAO.curie("0000231"),
    model_uri=OMOSCHEMA.has_obsolescence_reason,
    domain=None,
    range=Optional[str],
)

slots.consider = Slot(
    uri=OIO.consider,
    name="consider",
    curie=OIO.curie("consider"),
    model_uri=OMOSCHEMA.consider,
    domain=None,
    range=Optional[Union[Union[dict, Any], List[Union[dict, Any]]]],
)

slots.has_alternative_id = Slot(
    uri=OIO.hasAlternativeId,
    name="has_alternative_id",
    curie=OIO.curie("hasAlternativeId"),
    model_uri=OMOSCHEMA.has_alternative_id,
    domain=None,
    range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]],
)

slots.temporal_interpretation = Slot(
    uri=RO["0001900"],
    name="temporal_interpretation",
    curie=RO.curie("0001900"),
    model_uri=OMOSCHEMA.temporal_interpretation,
    domain=None,
    range=Optional[Union[str, NamedIndividualId]],
)

slots.never_in_taxon = Slot(
    uri=RO["0002161"],
    name="never_in_taxon",
    curie=RO.curie("0002161"),
    model_uri=OMOSCHEMA.never_in_taxon,
    domain=None,
    range=Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]],
)

slots.is_a_defining_property_chain_axiom = Slot(
    uri=RO["0002581"],
    name="is_a_defining_property_chain_axiom",
    curie=RO.curie("0002581"),
    model_uri=OMOSCHEMA.is_a_defining_property_chain_axiom,
    domain=None,
    range=Optional[str],
)

slots.is_a_defining_property_chain_axiom_where_second_argument_is_reflexive = Slot(
    uri=RO["0002582"],
    name="is_a_defining_property_chain_axiom_where_second_argument_is_reflexive",
    curie=RO.curie("0002582"),
    model_uri=OMOSCHEMA.is_a_defining_property_chain_axiom_where_second_argument_is_reflexive,
    domain=None,
    range=Optional[str],
)

slots.provenance_property = Slot(
    uri=OMOSCHEMA.provenance_property,
    name="provenance_property",
    curie=OMOSCHEMA.curie("provenance_property"),
    model_uri=OMOSCHEMA.provenance_property,
    domain=None,
    range=Optional[str],
)

slots.contributor = Slot(
    uri=DCTERMS.contributor,
    name="contributor",
    curie=DCTERMS.curie("contributor"),
    model_uri=OMOSCHEMA.contributor,
    domain=None,
    range=Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]],
)

slots.creator = Slot(
    uri=DCTERMS.creator,
    name="creator",
    curie=DCTERMS.curie("creator"),
    model_uri=OMOSCHEMA.creator,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.created = Slot(
    uri=DCTERMS.created,
    name="created",
    curie=DCTERMS.curie("created"),
    model_uri=OMOSCHEMA.created,
    domain=None,
    range=Optional[str],
)

slots.date = Slot(
    uri=DCTERMS.date,
    name="date",
    curie=DCTERMS.curie("date"),
    model_uri=OMOSCHEMA.date,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.source = Slot(
    uri=DCTERMS.source,
    name="source",
    curie=DCTERMS.curie("source"),
    model_uri=OMOSCHEMA.source,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.created_by = Slot(
    uri=OIO.created_by,
    name="created_by",
    curie=OIO.curie("created_by"),
    model_uri=OMOSCHEMA.created_by,
    domain=None,
    range=Optional[str],
)

slots.creation_date = Slot(
    uri=OIO.creation_date,
    name="creation_date",
    curie=OIO.curie("creation_date"),
    model_uri=OMOSCHEMA.creation_date,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.date_retrieved = Slot(
    uri=OIO.date_retrieved,
    name="date_retrieved",
    curie=OIO.curie("date_retrieved"),
    model_uri=OMOSCHEMA.date_retrieved,
    domain=None,
    range=Optional[str],
)

slots.editor_note = Slot(
    uri=IAO["0000116"],
    name="editor_note",
    curie=IAO.curie("0000116"),
    model_uri=OMOSCHEMA.editor_note,
    domain=None,
    range=Optional[Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]],
)

slots.term_editor = Slot(
    uri=IAO["0000117"],
    name="term_editor",
    curie=IAO.curie("0000117"),
    model_uri=OMOSCHEMA.term_editor,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.definition_source = Slot(
    uri=IAO["0000119"],
    name="definition_source",
    curie=IAO.curie("0000119"),
    model_uri=OMOSCHEMA.definition_source,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.curator_note = Slot(
    uri=IAO["0000232"],
    name="curator_note",
    curie=IAO.curie("0000232"),
    model_uri=OMOSCHEMA.curator_note,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.term_tracker_item = Slot(
    uri=IAO["0000233"],
    name="term_tracker_item",
    curie=IAO.curie("0000233"),
    model_uri=OMOSCHEMA.term_tracker_item,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.ontology_term_requester = Slot(
    uri=IAO["0000234"],
    name="ontology_term_requester",
    curie=IAO.curie("0000234"),
    model_uri=OMOSCHEMA.ontology_term_requester,
    domain=None,
    range=Optional[str],
)

slots.imported_from = Slot(
    uri=IAO["0000412"],
    name="imported_from",
    curie=IAO.curie("0000412"),
    model_uri=OMOSCHEMA.imported_from,
    domain=None,
    range=Optional[Union[Union[str, NamedIndividualId], List[Union[str, NamedIndividualId]]]],
)

slots.has_axiom_label = Slot(
    uri=IAO["0010000"],
    name="has_axiom_label",
    curie=IAO.curie("0010000"),
    model_uri=OMOSCHEMA.has_axiom_label,
    domain=None,
    range=Optional[Union[dict, Thing]],
)

slots.shortcut_annotation_property = Slot(
    uri=OMOSCHEMA.shortcut_annotation_property,
    name="shortcut_annotation_property",
    curie=OMOSCHEMA.curie("shortcut_annotation_property"),
    model_uri=OMOSCHEMA.shortcut_annotation_property,
    domain=None,
    range=Optional[str],
)

slots.disconnected_from = Slot(
    uri=OMOSCHEMA.disconnected_from,
    name="disconnected_from",
    curie=OMOSCHEMA.curie("disconnected_from"),
    model_uri=OMOSCHEMA.disconnected_from,
    domain=None,
    range=Optional[Union[str, ClassId]],
)

slots.excluded_axiom = Slot(
    uri=OMOSCHEMA.excluded_axiom,
    name="excluded_axiom",
    curie=OMOSCHEMA.curie("excluded_axiom"),
    model_uri=OMOSCHEMA.excluded_axiom,
    domain=None,
    range=Optional[str],
)

slots.excluded_from_QC_check = Slot(
    uri=OMOSCHEMA.excluded_from_QC_check,
    name="excluded_from_QC_check",
    curie=OMOSCHEMA.curie("excluded_from_QC_check"),
    model_uri=OMOSCHEMA.excluded_from_QC_check,
    domain=None,
    range=Optional[Union[dict, Thing]],
)

slots.excluded_subClassOf = Slot(
    uri=OMOSCHEMA.excluded_subClassOf,
    name="excluded_subClassOf",
    curie=OMOSCHEMA.curie("excluded_subClassOf"),
    model_uri=OMOSCHEMA.excluded_subClassOf,
    domain=None,
    range=Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]],
)

slots.excluded_synonym = Slot(
    uri=OMOSCHEMA.excluded_synonym,
    name="excluded_synonym",
    curie=OMOSCHEMA.curie("excluded_synonym"),
    model_uri=OMOSCHEMA.excluded_synonym,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.should_conform_to = Slot(
    uri=OMOSCHEMA.should_conform_to,
    name="should_conform_to",
    curie=OMOSCHEMA.curie("should_conform_to"),
    model_uri=OMOSCHEMA.should_conform_to,
    domain=None,
    range=Optional[Union[dict, Thing]],
)

slots.has_rank = Slot(
    uri=OMOSCHEMA.has_rank,
    name="has_rank",
    curie=OMOSCHEMA.curie("has_rank"),
    model_uri=OMOSCHEMA.has_rank,
    domain=None,
    range=Optional[Union[dict, Thing]],
)

slots.alternative_term = Slot(
    uri=IAO["0000118"],
    name="alternative_term",
    curie=IAO.curie("0000118"),
    model_uri=OMOSCHEMA.alternative_term,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.ISA_alternative_term = Slot(
    uri=OBI["0001847"],
    name="ISA_alternative_term",
    curie=OBI.curie("0001847"),
    model_uri=OMOSCHEMA.ISA_alternative_term,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.IEDB_alternative_term = Slot(
    uri=OBI["9991118"],
    name="IEDB_alternative_term",
    curie=OBI.curie("9991118"),
    model_uri=OMOSCHEMA.IEDB_alternative_term,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.OBO_foundry_unique_label = Slot(
    uri=IAO["0000589"],
    name="OBO_foundry_unique_label",
    curie=IAO.curie("0000589"),
    model_uri=OMOSCHEMA.OBO_foundry_unique_label,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.synonym = Slot(
    uri=OIO.hasSynonym,
    name="synonym",
    curie=OIO.curie("hasSynonym"),
    model_uri=OMOSCHEMA.synonym,
    domain=None,
    range=Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]],
)

slots.editor_preferred_term = Slot(
    uri=IAO["0000111"],
    name="editor_preferred_term",
    curie=IAO.curie("0000111"),
    model_uri=OMOSCHEMA.editor_preferred_term,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.has_exact_synonym = Slot(
    uri=OIO.hasExactSynonym,
    name="has_exact_synonym",
    curie=OIO.curie("hasExactSynonym"),
    model_uri=OMOSCHEMA.has_exact_synonym,
    domain=None,
    range=Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]],
)

slots.has_narrow_synonym = Slot(
    uri=OIO.hasNarrowSynonym,
    name="has_narrow_synonym",
    curie=OIO.curie("hasNarrowSynonym"),
    model_uri=OMOSCHEMA.has_narrow_synonym,
    domain=None,
    range=Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]],
)

slots.has_related_synonym = Slot(
    uri=OIO.hasRelatedSynonym,
    name="has_related_synonym",
    curie=OIO.curie("hasRelatedSynonym"),
    model_uri=OMOSCHEMA.has_related_synonym,
    domain=None,
    range=Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]],
)

slots.has_broad_synonym = Slot(
    uri=OIO.hasBroadSynonym,
    name="has_broad_synonym",
    curie=OIO.curie("hasBroadSynonym"),
    model_uri=OMOSCHEMA.has_broad_synonym,
    domain=None,
    range=Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]],
)

slots.has_synonym_type = Slot(
    uri=OIO.hasSynonymType,
    name="has_synonym_type",
    curie=OIO.curie("hasSynonymType"),
    model_uri=OMOSCHEMA.has_synonym_type,
    domain=None,
    range=Optional[Union[Union[str, AnnotationPropertyId], List[Union[str, AnnotationPropertyId]]]],
)

slots.has_obo_namespace = Slot(
    uri=OIO.hasOBONamespace,
    name="has_obo_namespace",
    curie=OIO.curie("hasOBONamespace"),
    model_uri=OMOSCHEMA.has_obo_namespace,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.in_subset = Slot(
    uri=OIO.inSubset,
    name="in_subset",
    curie=OIO.curie("inSubset"),
    model_uri=OMOSCHEMA.in_subset,
    domain=None,
    range=Optional[Union[Union[str, SubsetId], List[Union[str, SubsetId]]]],
)

slots.reification_predicate = Slot(
    uri=OMOSCHEMA.reification_predicate,
    name="reification_predicate",
    curie=OMOSCHEMA.curie("reification_predicate"),
    model_uri=OMOSCHEMA.reification_predicate,
    domain=None,
    range=Optional[str],
)

slots.annotatedProperty = Slot(
    uri=OWL.annotatedProperty,
    name="annotatedProperty",
    curie=OWL.curie("annotatedProperty"),
    model_uri=OMOSCHEMA.annotatedProperty,
    domain=None,
    range=Optional[Union[str, AnnotationPropertyId]],
)

slots.annotatedSource = Slot(
    uri=OWL.annotatedSource,
    name="annotatedSource",
    curie=OWL.curie("annotatedSource"),
    model_uri=OMOSCHEMA.annotatedSource,
    domain=None,
    range=Optional[Union[str, NamedObjectId]],
)

slots.annotatedTarget = Slot(
    uri=OWL.annotatedTarget,
    name="annotatedTarget",
    curie=OWL.curie("annotatedTarget"),
    model_uri=OMOSCHEMA.annotatedTarget,
    domain=None,
    range=Optional[Union[dict, Any]],
)

slots.imports = Slot(
    uri=OWL.imports,
    name="imports",
    curie=OWL.curie("imports"),
    model_uri=OMOSCHEMA.imports,
    domain=None,
    range=Optional[str],
)

slots.logical_predicate = Slot(
    uri=OMOSCHEMA.logical_predicate,
    name="logical_predicate",
    curie=OMOSCHEMA.curie("logical_predicate"),
    model_uri=OMOSCHEMA.logical_predicate,
    domain=None,
    range=Optional[str],
)

slots.cardinality = Slot(
    uri=OWL.cardinality,
    name="cardinality",
    curie=OWL.curie("cardinality"),
    model_uri=OMOSCHEMA.cardinality,
    domain=None,
    range=Optional[str],
)

slots.complementOf = Slot(
    uri=OWL.complementOf,
    name="complementOf",
    curie=OWL.curie("complementOf"),
    model_uri=OMOSCHEMA.complementOf,
    domain=None,
    range=Optional[str],
)

slots.disjointWith = Slot(
    uri=OWL.disjointWith,
    name="disjointWith",
    curie=OWL.curie("disjointWith"),
    model_uri=OMOSCHEMA.disjointWith,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.distinctMembers = Slot(
    uri=OWL.distinctMembers,
    name="distinctMembers",
    curie=OWL.curie("distinctMembers"),
    model_uri=OMOSCHEMA.distinctMembers,
    domain=None,
    range=Optional[Union[dict, Thing]],
)

slots.equivalentClass = Slot(
    uri=OWL.equivalentClass,
    name="equivalentClass",
    curie=OWL.curie("equivalentClass"),
    model_uri=OMOSCHEMA.equivalentClass,
    domain=None,
    range=Optional[Union[Union[dict, ClassExpression], List[Union[dict, ClassExpression]]]],
)

slots.sameAs = Slot(
    uri=OWL.sameAs,
    name="sameAs",
    curie=OWL.curie("sameAs"),
    model_uri=OMOSCHEMA.sameAs,
    domain=None,
    range=Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]],
)

slots.equivalentProperty = Slot(
    uri=OWL.equivalentProperty,
    name="equivalentProperty",
    curie=OWL.curie("equivalentProperty"),
    model_uri=OMOSCHEMA.equivalentProperty,
    domain=None,
    range=Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]],
)

slots.hasValue = Slot(
    uri=OWL.hasValue,
    name="hasValue",
    curie=OWL.curie("hasValue"),
    model_uri=OMOSCHEMA.hasValue,
    domain=None,
    range=Optional[Union[dict, Any]],
)

slots.intersectionOf = Slot(
    uri=OWL.intersectionOf,
    name="intersectionOf",
    curie=OWL.curie("intersectionOf"),
    model_uri=OMOSCHEMA.intersectionOf,
    domain=None,
    range=Optional[Union[dict, ClassExpression]],
)

slots.inverseOf = Slot(
    uri=OWL.inverseOf,
    name="inverseOf",
    curie=OWL.curie("inverseOf"),
    model_uri=OMOSCHEMA.inverseOf,
    domain=None,
    range=Optional[Union[str, PropertyId]],
)

slots.maxQualifiedCardinality = Slot(
    uri=OWL.maxQualifiedCardinality,
    name="maxQualifiedCardinality",
    curie=OWL.curie("maxQualifiedCardinality"),
    model_uri=OMOSCHEMA.maxQualifiedCardinality,
    domain=None,
    range=Optional[int],
)

slots.members = Slot(
    uri=OWL.members,
    name="members",
    curie=OWL.curie("members"),
    model_uri=OMOSCHEMA.members,
    domain=None,
    range=Optional[Union[dict, Thing]],
)

slots.minCardinality = Slot(
    uri=OWL.minCardinality,
    name="minCardinality",
    curie=OWL.curie("minCardinality"),
    model_uri=OMOSCHEMA.minCardinality,
    domain=None,
    range=Optional[int],
)

slots.minQualifiedCardinality = Slot(
    uri=OWL.minQualifiedCardinality,
    name="minQualifiedCardinality",
    curie=OWL.curie("minQualifiedCardinality"),
    model_uri=OMOSCHEMA.minQualifiedCardinality,
    domain=None,
    range=Optional[int],
)

slots.onClass = Slot(
    uri=OWL.onClass,
    name="onClass",
    curie=OWL.curie("onClass"),
    model_uri=OMOSCHEMA.onClass,
    domain=None,
    range=Optional[Union[dict, ClassExpression]],
)

slots.onProperty = Slot(
    uri=OWL.onProperty,
    name="onProperty",
    curie=OWL.curie("onProperty"),
    model_uri=OMOSCHEMA.onProperty,
    domain=None,
    range=Optional[Union[Union[dict, PropertyExpression], List[Union[dict, PropertyExpression]]]],
)

slots.oneOf = Slot(
    uri=OWL.oneOf,
    name="oneOf",
    curie=OWL.curie("oneOf"),
    model_uri=OMOSCHEMA.oneOf,
    domain=None,
    range=Optional[Union[dict, ClassExpression]],
)

slots.propertyChainAxiom = Slot(
    uri=OWL.propertyChainAxiom,
    name="propertyChainAxiom",
    curie=OWL.curie("propertyChainAxiom"),
    model_uri=OMOSCHEMA.propertyChainAxiom,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.qualifiedCardinality = Slot(
    uri=OWL.qualifiedCardinality,
    name="qualifiedCardinality",
    curie=OWL.curie("qualifiedCardinality"),
    model_uri=OMOSCHEMA.qualifiedCardinality,
    domain=None,
    range=Optional[str],
)

slots.allValuesFrom = Slot(
    uri=OWL.allValuesFrom,
    name="allValuesFrom",
    curie=OWL.curie("allValuesFrom"),
    model_uri=OMOSCHEMA.allValuesFrom,
    domain=None,
    range=Optional[str],
)

slots.someValuesFrom = Slot(
    uri=OWL.someValuesFrom,
    name="someValuesFrom",
    curie=OWL.curie("someValuesFrom"),
    model_uri=OMOSCHEMA.someValuesFrom,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.unionOf = Slot(
    uri=OWL.unionOf,
    name="unionOf",
    curie=OWL.curie("unionOf"),
    model_uri=OMOSCHEMA.unionOf,
    domain=None,
    range=Optional[str],
)

slots.domain = Slot(
    uri=RDFS.domain,
    name="domain",
    curie=RDFS.curie("domain"),
    model_uri=OMOSCHEMA.domain,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.range = Slot(
    uri=RDFS.range,
    name="range",
    curie=RDFS.curie("range"),
    model_uri=OMOSCHEMA.range,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.isDefinedBy = Slot(
    uri=RDFS.isDefinedBy,
    name="isDefinedBy",
    curie=RDFS.curie("isDefinedBy"),
    model_uri=OMOSCHEMA.isDefinedBy,
    domain=None,
    range=Optional[Union[str, OntologyId]],
)

slots.seeAlso = Slot(
    uri=RDFS.seeAlso,
    name="seeAlso",
    curie=RDFS.curie("seeAlso"),
    model_uri=OMOSCHEMA.seeAlso,
    domain=None,
    range=Optional[Union[Union[dict, Thing], List[Union[dict, Thing]]]],
)

slots.type = Slot(
    uri=RDF.type,
    name="type",
    curie=RDF.curie("type"),
    model_uri=OMOSCHEMA.type,
    domain=None,
    range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]],
)

slots.subClassOf = Slot(
    uri=RDFS.subClassOf,
    name="subClassOf",
    curie=RDFS.curie("subClassOf"),
    model_uri=OMOSCHEMA.subClassOf,
    domain=None,
    range=Optional[Union[Union[dict, ClassExpression], List[Union[dict, ClassExpression]]]],
)

slots.oboInOwl_id = Slot(
    uri=OIO.id,
    name="oboInOwl_id",
    curie=OIO.curie("id"),
    model_uri=OMOSCHEMA.oboInOwl_id,
    domain=None,
    range=Optional[str],
)

slots.oboInOwl_ontology = Slot(
    uri=OIO.ontology,
    name="oboInOwl_ontology",
    curie=OIO.curie("ontology"),
    model_uri=OMOSCHEMA.oboInOwl_ontology,
    domain=None,
    range=Optional[str],
)

slots.is_class_level = Slot(
    uri=OIO.is_class_level,
    name="is_class_level",
    curie=OIO.curie("is_class_level"),
    model_uri=OMOSCHEMA.is_class_level,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.is_cyclic = Slot(
    uri=OIO.is_cyclic,
    name="is_cyclic",
    curie=OIO.curie("is_cyclic"),
    model_uri=OMOSCHEMA.is_cyclic,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.is_inferred = Slot(
    uri=OIO.is_inferred,
    name="is_inferred",
    curie=OIO.curie("is_inferred"),
    model_uri=OMOSCHEMA.is_inferred,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.is_metadata_tag = Slot(
    uri=OIO.is_metadata_tag,
    name="is_metadata_tag",
    curie=OIO.curie("is_metadata_tag"),
    model_uri=OMOSCHEMA.is_metadata_tag,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.is_transitive = Slot(
    uri=OIO.is_transitive,
    name="is_transitive",
    curie=OIO.curie("is_transitive"),
    model_uri=OMOSCHEMA.is_transitive,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.notes = Slot(
    uri=OIO.notes,
    name="notes",
    curie=OIO.curie("notes"),
    model_uri=OMOSCHEMA.notes,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.shorthand = Slot(
    uri=OIO.shorthand,
    name="shorthand",
    curie=OIO.curie("shorthand"),
    model_uri=OMOSCHEMA.shorthand,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.url = Slot(
    uri=OIO.url,
    name="url",
    curie=OIO.curie("url"),
    model_uri=OMOSCHEMA.url,
    domain=None,
    range=Optional[str],
)

slots.evidence = Slot(
    uri=OIO.evidence,
    name="evidence",
    curie=OIO.curie("evidence"),
    model_uri=OMOSCHEMA.evidence,
    domain=None,
    range=Optional[str],
)

slots.external_ontology = Slot(
    uri=OIO.external_ontology,
    name="external_ontology",
    curie=OIO.curie("external_ontology"),
    model_uri=OMOSCHEMA.external_ontology,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.NCIT_definition_source = Slot(
    uri=NCIT.P378,
    name="NCIT_definition_source",
    curie=NCIT.curie("P378"),
    model_uri=OMOSCHEMA.NCIT_definition_source,
    domain=None,
    range=Optional[str],
)

slots.NCIT_term_type = Slot(
    uri=NCIT.P383,
    name="NCIT_term_type",
    curie=NCIT.curie("P383"),
    model_uri=OMOSCHEMA.NCIT_term_type,
    domain=None,
    range=Optional[str],
)

slots.NCIT_term_source = Slot(
    uri=NCIT.P384,
    name="NCIT_term_source",
    curie=NCIT.curie("P384"),
    model_uri=OMOSCHEMA.NCIT_term_source,
    domain=None,
    range=Optional[str],
)

slots.annotation__predicate = Slot(
    uri=OMOSCHEMA.predicate,
    name="annotation__predicate",
    curie=OMOSCHEMA.curie("predicate"),
    model_uri=OMOSCHEMA.annotation__predicate,
    domain=None,
    range=Optional[str],
)

slots.annotation__object = Slot(
    uri=OMOSCHEMA.object,
    name="annotation__object",
    curie=OMOSCHEMA.curie("object"),
    model_uri=OMOSCHEMA.annotation__object,
    domain=None,
    range=Optional[str],
)

slots.Ontology_title = Slot(
    uri=DCTERMS.title,
    name="Ontology_title",
    curie=DCTERMS.curie("title"),
    model_uri=OMOSCHEMA.Ontology_title,
    domain=Ontology,
    range=Union[str, NarrativeText],
)

slots.Ontology_license = Slot(
    uri=DCTERMS.license,
    name="Ontology_license",
    curie=DCTERMS.curie("license"),
    model_uri=OMOSCHEMA.Ontology_license,
    domain=Ontology,
    range=Union[dict, Thing],
)

slots.Ontology_versionIRI = Slot(
    uri=OWL.versionIRI,
    name="Ontology_versionIRI",
    curie=OWL.curie("versionIRI"),
    model_uri=OMOSCHEMA.Ontology_versionIRI,
    domain=Ontology,
    range=Union[str, URIorCURIE],
)

slots.Ontology_versionInfo = Slot(
    uri=OWL.versionInfo,
    name="Ontology_versionInfo",
    curie=OWL.curie("versionInfo"),
    model_uri=OMOSCHEMA.Ontology_versionInfo,
    domain=Ontology,
    range=str,
)

slots.Class_label = Slot(
    uri=RDFS.label,
    name="Class_label",
    curie=RDFS.curie("label"),
    model_uri=OMOSCHEMA.Class_label,
    domain=Class,
    range=Union[str, LabelType],
)

slots.Class_definition = Slot(
    uri=IAO["0000115"],
    name="Class_definition",
    curie=IAO.curie("0000115"),
    model_uri=OMOSCHEMA.Class_definition,
    domain=Class,
    range=Optional[Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]],
)

slots.Class_broadMatch = Slot(
    uri=SKOS.broadMatch,
    name="Class_broadMatch",
    curie=SKOS.curie("broadMatch"),
    model_uri=OMOSCHEMA.Class_broadMatch,
    domain=Class,
    range=Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]],
)

slots.Class_exactMatch = Slot(
    uri=SKOS.exactMatch,
    name="Class_exactMatch",
    curie=SKOS.curie("exactMatch"),
    model_uri=OMOSCHEMA.Class_exactMatch,
    domain=Class,
    range=Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]],
)

slots.Class_narrowMatch = Slot(
    uri=SKOS.narrowMatch,
    name="Class_narrowMatch",
    curie=SKOS.curie("narrowMatch"),
    model_uri=OMOSCHEMA.Class_narrowMatch,
    domain=Class,
    range=Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]],
)

slots.Class_closeMatch = Slot(
    uri=SKOS.closeMatch,
    name="Class_closeMatch",
    curie=SKOS.curie("closeMatch"),
    model_uri=OMOSCHEMA.Class_closeMatch,
    domain=Class,
    range=Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]],
)

slots.Class_subClassOf = Slot(
    uri=RDFS.subClassOf,
    name="Class_subClassOf",
    curie=RDFS.curie("subClassOf"),
    model_uri=OMOSCHEMA.Class_subClassOf,
    domain=Class,
    range=Optional[Union[Union[str, ClassId], List[Union[str, ClassId]]]],
)

slots.Property_label = Slot(
    uri=RDFS.label,
    name="Property_label",
    curie=RDFS.curie("label"),
    model_uri=OMOSCHEMA.Property_label,
    domain=Property,
    range=Optional[Union[str, LabelType]],
)

slots.Property_definition = Slot(
    uri=IAO["0000115"],
    name="Property_definition",
    curie=IAO.curie("0000115"),
    model_uri=OMOSCHEMA.Property_definition,
    domain=Property,
    range=Optional[Union[Union[str, NarrativeText], List[Union[str, NarrativeText]]]],
)

slots.Property_broadMatch = Slot(
    uri=SKOS.broadMatch,
    name="Property_broadMatch",
    curie=SKOS.curie("broadMatch"),
    model_uri=OMOSCHEMA.Property_broadMatch,
    domain=Property,
    range=Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]],
)

slots.Property_exactMatch = Slot(
    uri=SKOS.exactMatch,
    name="Property_exactMatch",
    curie=SKOS.curie("exactMatch"),
    model_uri=OMOSCHEMA.Property_exactMatch,
    domain=Property,
    range=Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]],
)

slots.Property_narrowMatch = Slot(
    uri=SKOS.narrowMatch,
    name="Property_narrowMatch",
    curie=SKOS.curie("narrowMatch"),
    model_uri=OMOSCHEMA.Property_narrowMatch,
    domain=Property,
    range=Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]],
)

slots.Property_closeMatch = Slot(
    uri=SKOS.closeMatch,
    name="Property_closeMatch",
    curie=SKOS.curie("closeMatch"),
    model_uri=OMOSCHEMA.Property_closeMatch,
    domain=Property,
    range=Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]],
)

slots.Property_subClassOf = Slot(
    uri=RDFS.subClassOf,
    name="Property_subClassOf",
    curie=RDFS.curie("subClassOf"),
    model_uri=OMOSCHEMA.Property_subClassOf,
    domain=Property,
    range=Optional[Union[Union[str, PropertyId], List[Union[str, PropertyId]]]],
)

slots.Axiom_database_cross_reference = Slot(
    uri=OIO.hasDbXref,
    name="Axiom_database_cross_reference",
    curie=OIO.curie("hasDbXref"),
    model_uri=OMOSCHEMA.Axiom_database_cross_reference,
    domain=Axiom,
    range=Optional[Union[Union[str, CURIELiteral], List[Union[str, CURIELiteral]]]],
)

slots.ObsoleteAspect_label = Slot(
    uri=RDFS.label,
    name="ObsoleteAspect_label",
    curie=RDFS.curie("label"),
    model_uri=OMOSCHEMA.ObsoleteAspect_label,
    domain=None,
    range=Optional[Union[str, LabelType]],
    pattern=re.compile(r"^obsolete"),
)
