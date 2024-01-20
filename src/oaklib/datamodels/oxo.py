# Auto generated from oxo.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-04-12T11:15:58
# Schema: oxo-schema
#
# id: https://w3id.org/sssom/oxo
# description: Schema for OLS OXO payloads
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import as_dict
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue
from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.metamodelcore import empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from rdflib import URIRef

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OXO = CurieNamespace("oxo", "https://w3id.org/sssom/oxo/")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = OXO


# Types
class HttpsIdentifier(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "https identifier"
    type_model_uri = OXO.HttpsIdentifier


class OntologyIdentifier(Uriorcurie):
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "OntologyIdentifier"
    type_model_uri = OXO.OntologyIdentifier


class HttpIdentifier(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "http identifier"
    type_model_uri = OXO.HttpIdentifier


class Identifier(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "identifier"
    type_model_uri = OXO.Identifier


# Class references
class TermCurie(extended_str):
    pass


@dataclass
class Datasource(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OXO.Datasource
    class_class_curie: ClassVar[str] = "oxo:Datasource"
    class_name: ClassVar[str] = "Datasource"
    class_model_uri: ClassVar[URIRef] = OXO.Datasource

    prefix: Optional[str] = None
    preferredPrefix: Optional[str] = None
    idorgNamespace: Optional[str] = None
    alternatePrefix: Optional[Union[str, List[str]]] = empty_list()
    alternateIris: Optional[Union[str, List[str]]] = empty_list()
    name: Optional[str] = None
    orcid: Optional[str] = None
    description: Optional[str] = None
    source: Optional[Union[str, "SourceEnum"]] = None
    licence: Optional[Union[str, HttpsIdentifier]] = None
    versionInfo: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.prefix is not None and not isinstance(self.prefix, str):
            self.prefix = str(self.prefix)

        if self.preferredPrefix is not None and not isinstance(self.preferredPrefix, str):
            self.preferredPrefix = str(self.preferredPrefix)

        if self.idorgNamespace is not None and not isinstance(self.idorgNamespace, str):
            self.idorgNamespace = str(self.idorgNamespace)

        if not isinstance(self.alternatePrefix, list):
            self.alternatePrefix = (
                [self.alternatePrefix] if self.alternatePrefix is not None else []
            )
        self.alternatePrefix = [v if isinstance(v, str) else str(v) for v in self.alternatePrefix]

        if not isinstance(self.alternateIris, list):
            self.alternateIris = [self.alternateIris] if self.alternateIris is not None else []
        self.alternateIris = [v if isinstance(v, str) else str(v) for v in self.alternateIris]

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.orcid is not None and not isinstance(self.orcid, str):
            self.orcid = str(self.orcid)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.source is not None and not isinstance(self.source, SourceEnum):
            self.source = SourceEnum(self.source)

        if self.licence is not None and not isinstance(self.licence, HttpsIdentifier):
            self.licence = HttpsIdentifier(self.licence)

        if self.versionInfo is not None and not isinstance(self.versionInfo, str):
            self.versionInfo = str(self.versionInfo)

        super().__post_init__(**kwargs)


@dataclass
class Term(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OXO.Term
    class_class_curie: ClassVar[str] = "oxo:Term"
    class_name: ClassVar[str] = "Term"
    class_model_uri: ClassVar[URIRef] = OXO.Term

    curie: Union[str, TermCurie] = None
    identifier: Optional[str] = None
    uri: Optional[Union[str, HttpIdentifier]] = None
    label: Optional[str] = None
    datasource: Optional[Union[dict, Datasource]] = None
    href: Optional[Union[str, HttpsIdentifier]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.curie):
            self.MissingRequiredField("curie")
        if not isinstance(self.curie, TermCurie):
            self.curie = TermCurie(self.curie)

        if self.identifier is not None and not isinstance(self.identifier, str):
            self.identifier = str(self.identifier)

        if self.uri is not None and not isinstance(self.uri, HttpIdentifier):
            self.uri = HttpIdentifier(self.uri)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.datasource is not None and not isinstance(self.datasource, Datasource):
            self.datasource = Datasource(**as_dict(self.datasource))

        if self.href is not None and not isinstance(self.href, HttpsIdentifier):
            self.href = HttpsIdentifier(self.href)

        super().__post_init__(**kwargs)


@dataclass
class Link(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OXO.Link
    class_class_curie: ClassVar[str] = "oxo:Link"
    class_name: ClassVar[str] = "Link"
    class_model_uri: ClassVar[URIRef] = OXO.Link

    href: Optional[Union[str, HttpsIdentifier]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.href is not None and not isinstance(self.href, HttpsIdentifier):
            self.href = HttpsIdentifier(self.href)

        super().__post_init__(**kwargs)


@dataclass
class LinkSet(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OXO.LinkSet
    class_class_curie: ClassVar[str] = "oxo:LinkSet"
    class_name: ClassVar[str] = "LinkSet"
    class_model_uri: ClassVar[URIRef] = OXO.LinkSet

    link_to_self: Optional[Union[dict, Link]] = None
    fromTerm: Optional[Union[dict, Link]] = None
    toTerm: Optional[Union[dict, Link]] = None
    first: Optional[Union[dict, Link]] = None
    next: Optional[Union[dict, Link]] = None
    last: Optional[Union[dict, Link]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.link_to_self is not None and not isinstance(self.link_to_self, Link):
            self.link_to_self = Link(**as_dict(self.link_to_self))

        if self.fromTerm is not None and not isinstance(self.fromTerm, Link):
            self.fromTerm = Link(**as_dict(self.fromTerm))

        if self.toTerm is not None and not isinstance(self.toTerm, Link):
            self.toTerm = Link(**as_dict(self.toTerm))

        if self.first is not None and not isinstance(self.first, Link):
            self.first = Link(**as_dict(self.first))

        if self.next is not None and not isinstance(self.next, Link):
            self.next = Link(**as_dict(self.next))

        if self.last is not None and not isinstance(self.last, Link):
            self.last = Link(**as_dict(self.last))

        super().__post_init__(**kwargs)


@dataclass
class Mapping(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OXO.Mapping
    class_class_curie: ClassVar[str] = "oxo:Mapping"
    class_name: ClassVar[str] = "Mapping"
    class_model_uri: ClassVar[URIRef] = OXO.Mapping

    mappingId: Optional[int] = None
    datasource: Optional[Union[dict, Datasource]] = None
    sourcePrefix: Optional[str] = None
    sourceType: Optional[Union[str, "SourceEnum"]] = None
    predicate: Optional[str] = None
    fromTerm: Optional[Union[dict, Term]] = None
    toTerm: Optional[Union[dict, Term]] = None
    scope: Optional[Union[str, "ScopeEnum"]] = None
    date: Optional[str] = None
    _links: Optional[Union[dict, LinkSet]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.mappingId is not None and not isinstance(self.mappingId, int):
            self.mappingId = int(self.mappingId)

        if self.datasource is not None and not isinstance(self.datasource, Datasource):
            self.datasource = Datasource(**as_dict(self.datasource))

        if self.sourcePrefix is not None and not isinstance(self.sourcePrefix, str):
            self.sourcePrefix = str(self.sourcePrefix)

        if self.sourceType is not None and not isinstance(self.sourceType, SourceEnum):
            self.sourceType = SourceEnum(self.sourceType)

        if self.predicate is not None and not isinstance(self.predicate, str):
            self.predicate = str(self.predicate)

        if self.fromTerm is not None and not isinstance(self.fromTerm, Term):
            self.fromTerm = Term(**as_dict(self.fromTerm))

        if self.toTerm is not None and not isinstance(self.toTerm, Term):
            self.toTerm = Term(**as_dict(self.toTerm))

        if self.scope is not None and not isinstance(self.scope, ScopeEnum):
            self.scope = ScopeEnum(self.scope)

        if self.date is not None and not isinstance(self.date, str):
            self.date = str(self.date)

        if self._links is not None and not isinstance(self._links, LinkSet):
            self._links = LinkSet(**as_dict(self._links))

        super().__post_init__(**kwargs)


@dataclass
class Embedded(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OXO.Embedded
    class_class_curie: ClassVar[str] = "oxo:Embedded"
    class_name: ClassVar[str] = "Embedded"
    class_model_uri: ClassVar[URIRef] = OXO.Embedded

    mappings: Optional[Union[Union[dict, Mapping], List[Union[dict, Mapping]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.mappings, list):
            self.mappings = [self.mappings] if self.mappings is not None else []
        self.mappings = [
            v if isinstance(v, Mapping) else Mapping(**as_dict(v)) for v in self.mappings
        ]

        super().__post_init__(**kwargs)


@dataclass
class Page(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OXO.Page
    class_class_curie: ClassVar[str] = "oxo:Page"
    class_name: ClassVar[str] = "Page"
    class_model_uri: ClassVar[URIRef] = OXO.Page

    size: Optional[int] = None
    totalElements: Optional[int] = None
    totalPages: Optional[int] = None
    number: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.size is not None and not isinstance(self.size, int):
            self.size = int(self.size)

        if self.totalElements is not None and not isinstance(self.totalElements, int):
            self.totalElements = int(self.totalElements)

        if self.totalPages is not None and not isinstance(self.totalPages, int):
            self.totalPages = int(self.totalPages)

        if self.number is not None and not isinstance(self.number, int):
            self.number = int(self.number)

        super().__post_init__(**kwargs)


@dataclass
class Container(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OXO.Container
    class_class_curie: ClassVar[str] = "oxo:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = OXO.Container

    _embedded: Optional[Union[dict, Embedded]] = None
    _links: Optional[Union[dict, LinkSet]] = None
    page: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._embedded is not None and not isinstance(self._embedded, Embedded):
            self._embedded = Embedded(**as_dict(self._embedded))

        if self._links is not None and not isinstance(self._links, LinkSet):
            self._links = LinkSet(**as_dict(self._links))

        if self.page is not None and not isinstance(self.page, str):
            self.page = str(self.page)

        super().__post_init__(**kwargs)


# Enumerations
class SourceEnum(EnumDefinitionImpl):
    ONTOLOGY = PermissibleValue(text="ONTOLOGY")
    DATABASE = PermissibleValue(text="DATABASE")

    _defn = EnumDefinition(
        name="SourceEnum",
    )


class ScopeEnum(EnumDefinitionImpl):
    RELATED = PermissibleValue(text="RELATED")
    EXACT = PermissibleValue(text="EXACT")
    BROADER = PermissibleValue(text="BROADER")
    NARROWER = PermissibleValue(text="NARROWER")
    LABEL = PermissibleValue(text="LABEL")

    _defn = EnumDefinition(
        name="ScopeEnum",
    )


# Slots
class slots:
    pass


slots.prefix = Slot(
    uri=OXO.prefix,
    name="prefix",
    curie=OXO.curie("prefix"),
    model_uri=OXO.prefix,
    domain=None,
    range=Optional[str],
)

slots.preferredPrefix = Slot(
    uri=OXO.preferredPrefix,
    name="preferredPrefix",
    curie=OXO.curie("preferredPrefix"),
    model_uri=OXO.preferredPrefix,
    domain=None,
    range=Optional[str],
)

slots.idorgNamespace = Slot(
    uri=OXO.idorgNamespace,
    name="idorgNamespace",
    curie=OXO.curie("idorgNamespace"),
    model_uri=OXO.idorgNamespace,
    domain=None,
    range=Optional[str],
)

slots.alternatePrefix = Slot(
    uri=OXO.alternatePrefix,
    name="alternatePrefix",
    curie=OXO.curie("alternatePrefix"),
    model_uri=OXO.alternatePrefix,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.alternateIris = Slot(
    uri=OXO.alternateIris,
    name="alternateIris",
    curie=OXO.curie("alternateIris"),
    model_uri=OXO.alternateIris,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.name = Slot(
    uri=OXO.name,
    name="name",
    curie=OXO.curie("name"),
    model_uri=OXO.name,
    domain=None,
    range=Optional[str],
)

slots.orcid = Slot(
    uri=OXO.orcid,
    name="orcid",
    curie=OXO.curie("orcid"),
    model_uri=OXO.orcid,
    domain=None,
    range=Optional[str],
)

slots.description = Slot(
    uri=OXO.description,
    name="description",
    curie=OXO.curie("description"),
    model_uri=OXO.description,
    domain=None,
    range=Optional[str],
)

slots.source = Slot(
    uri=OXO.source,
    name="source",
    curie=OXO.curie("source"),
    model_uri=OXO.source,
    domain=None,
    range=Optional[Union[str, "SourceEnum"]],
)

slots.licence = Slot(
    uri=OXO.licence,
    name="licence",
    curie=OXO.curie("licence"),
    model_uri=OXO.licence,
    domain=None,
    range=Optional[Union[str, HttpsIdentifier]],
)

slots.versionInfo = Slot(
    uri=OXO.versionInfo,
    name="versionInfo",
    curie=OXO.curie("versionInfo"),
    model_uri=OXO.versionInfo,
    domain=None,
    range=Optional[str],
)

slots.curie = Slot(
    uri=OXO.curie,
    name="curie",
    curie=OXO.curie("curie"),
    model_uri=OXO.curie,
    domain=None,
    range=URIRef,
)

slots.identifier = Slot(
    uri=OXO.identifier,
    name="identifier",
    curie=OXO.curie("identifier"),
    model_uri=OXO.identifier,
    domain=None,
    range=Optional[str],
)

slots.uri = Slot(
    uri=OXO.uri,
    name="uri",
    curie=OXO.curie("uri"),
    model_uri=OXO.uri,
    domain=None,
    range=Optional[Union[str, HttpIdentifier]],
)

slots.label = Slot(
    uri=OXO.label,
    name="label",
    curie=OXO.curie("label"),
    model_uri=OXO.label,
    domain=None,
    range=Optional[str],
)

slots.datasource = Slot(
    uri=OXO.datasource,
    name="datasource",
    curie=OXO.curie("datasource"),
    model_uri=OXO.datasource,
    domain=None,
    range=Optional[Union[dict, Datasource]],
)

slots.href = Slot(
    uri=OXO.href,
    name="href",
    curie=OXO.curie("href"),
    model_uri=OXO.href,
    domain=None,
    range=Optional[Union[str, HttpsIdentifier]],
)

slots.first = Slot(
    uri=OXO.first,
    name="first",
    curie=OXO.curie("first"),
    model_uri=OXO.first,
    domain=None,
    range=Optional[Union[dict, Link]],
)

slots.next = Slot(
    uri=OXO.next,
    name="next",
    curie=OXO.curie("next"),
    model_uri=OXO.next,
    domain=None,
    range=Optional[Union[dict, Link]],
)

slots.last = Slot(
    uri=OXO.last,
    name="last",
    curie=OXO.curie("last"),
    model_uri=OXO.last,
    domain=None,
    range=Optional[Union[dict, Link]],
)

slots.link_to_self = Slot(
    uri=OXO.link_to_self,
    name="link_to_self",
    curie=OXO.curie("link_to_self"),
    model_uri=OXO.link_to_self,
    domain=None,
    range=Optional[Union[dict, Link]],
)

slots.fromTerm = Slot(
    uri=OXO.fromTerm,
    name="fromTerm",
    curie=OXO.curie("fromTerm"),
    model_uri=OXO.fromTerm,
    domain=None,
    range=Optional[Union[str, TermCurie]],
)

slots.toTerm = Slot(
    uri=OXO.toTerm,
    name="toTerm",
    curie=OXO.curie("toTerm"),
    model_uri=OXO.toTerm,
    domain=None,
    range=Optional[Union[str, TermCurie]],
)

slots.mappingId = Slot(
    uri=OXO.mappingId,
    name="mappingId",
    curie=OXO.curie("mappingId"),
    model_uri=OXO.mappingId,
    domain=None,
    range=Optional[int],
)

slots.sourcePrefix = Slot(
    uri=OXO.sourcePrefix,
    name="sourcePrefix",
    curie=OXO.curie("sourcePrefix"),
    model_uri=OXO.sourcePrefix,
    domain=None,
    range=Optional[str],
)

slots.sourceType = Slot(
    uri=OXO.sourceType,
    name="sourceType",
    curie=OXO.curie("sourceType"),
    model_uri=OXO.sourceType,
    domain=None,
    range=Optional[Union[str, "SourceEnum"]],
)

slots.predicate = Slot(
    uri=OXO.predicate,
    name="predicate",
    curie=OXO.curie("predicate"),
    model_uri=OXO.predicate,
    domain=None,
    range=Optional[str],
)

slots.scope = Slot(
    uri=OXO.scope,
    name="scope",
    curie=OXO.curie("scope"),
    model_uri=OXO.scope,
    domain=None,
    range=Optional[Union[str, "ScopeEnum"]],
)

slots.date = Slot(
    uri=OXO.date,
    name="date",
    curie=OXO.curie("date"),
    model_uri=OXO.date,
    domain=None,
    range=Optional[str],
)

slots._links = Slot(
    uri=OXO._links,
    name="_links",
    curie=OXO.curie("_links"),
    model_uri=OXO._links,
    domain=None,
    range=Optional[Union[dict, LinkSet]],
)

slots.mappings = Slot(
    uri=OXO.mappings,
    name="mappings",
    curie=OXO.curie("mappings"),
    model_uri=OXO.mappings,
    domain=None,
    range=Optional[Union[Union[dict, Mapping], List[Union[dict, Mapping]]]],
)

slots.size = Slot(
    uri=OXO.size,
    name="size",
    curie=OXO.curie("size"),
    model_uri=OXO.size,
    domain=None,
    range=Optional[int],
)

slots.totalElements = Slot(
    uri=OXO.totalElements,
    name="totalElements",
    curie=OXO.curie("totalElements"),
    model_uri=OXO.totalElements,
    domain=None,
    range=Optional[int],
)

slots.totalPages = Slot(
    uri=OXO.totalPages,
    name="totalPages",
    curie=OXO.curie("totalPages"),
    model_uri=OXO.totalPages,
    domain=None,
    range=Optional[int],
)

slots.number = Slot(
    uri=OXO.number,
    name="number",
    curie=OXO.curie("number"),
    model_uri=OXO.number,
    domain=None,
    range=Optional[int],
)

slots._embedded = Slot(
    uri=OXO._embedded,
    name="_embedded",
    curie=OXO.curie("_embedded"),
    model_uri=OXO._embedded,
    domain=None,
    range=Optional[Union[dict, Embedded]],
)

slots.page = Slot(
    uri=OXO.page,
    name="page",
    curie=OXO.curie("page"),
    model_uri=OXO.page,
    domain=None,
    range=Optional[str],
)

slots.LinkSet_fromTerm = Slot(
    uri=OXO.fromTerm,
    name="LinkSet_fromTerm",
    curie=OXO.curie("fromTerm"),
    model_uri=OXO.LinkSet_fromTerm,
    domain=LinkSet,
    range=Optional[Union[dict, Link]],
)

slots.LinkSet_toTerm = Slot(
    uri=OXO.toTerm,
    name="LinkSet_toTerm",
    curie=OXO.curie("toTerm"),
    model_uri=OXO.LinkSet_toTerm,
    domain=LinkSet,
    range=Optional[Union[dict, Link]],
)

slots.LinkSet_first = Slot(
    uri=OXO.first,
    name="LinkSet_first",
    curie=OXO.curie("first"),
    model_uri=OXO.LinkSet_first,
    domain=LinkSet,
    range=Optional[Union[dict, Link]],
)

slots.LinkSet_next = Slot(
    uri=OXO.next,
    name="LinkSet_next",
    curie=OXO.curie("next"),
    model_uri=OXO.LinkSet_next,
    domain=LinkSet,
    range=Optional[Union[dict, Link]],
)

slots.LinkSet_last = Slot(
    uri=OXO.last,
    name="LinkSet_last",
    curie=OXO.curie("last"),
    model_uri=OXO.LinkSet_last,
    domain=LinkSet,
    range=Optional[Union[dict, Link]],
)

slots.Mapping_fromTerm = Slot(
    uri=OXO.fromTerm,
    name="Mapping_fromTerm",
    curie=OXO.curie("fromTerm"),
    model_uri=OXO.Mapping_fromTerm,
    domain=Mapping,
    range=Optional[Union[dict, Term]],
)

slots.Mapping_toTerm = Slot(
    uri=OXO.toTerm,
    name="Mapping_toTerm",
    curie=OXO.curie("toTerm"),
    model_uri=OXO.Mapping_toTerm,
    domain=Mapping,
    range=Optional[Union[dict, Term]],
)
