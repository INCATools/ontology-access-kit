# Auto generated from fhir.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-11-30T14:50:13
# Schema: fhir
#
# id: https://w3id.org/linkml/fhir
# description: Schema for working with FHIR objects
# license: https://creativecommons.org/publicdomain/zero/1.0/
import dataclasses
import re
import sys
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions,
)
from linkml_runtime.linkml_model.types import Boolean, Datetime, String, Uri
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import (
    URI,
    Bool,
    XSDDateTime,
    bnode,
    empty_dict,
    empty_list,
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str,
)
from rdflib import Namespace, URIRef

metamodel_version = "1.7.0"
version = "0.0.1"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
FHIR = CurieNamespace("fhir", "https://w3id.org/linkml/fhir/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OG = CurieNamespace("og", "https://github.com/geneontology/obographs/")
OIO = CurieNamespace("oio", "http://www.geneontology.org/formats/oboInOwl#")
SDO = CurieNamespace("sdo", "https://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
DEFAULT_ = FHIR


# Types

# Class references


@dataclass
class CodeSystem(YAMLRoot):
    """
    Declares the existence of and describes a code system or code system supplement
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FHIR.CodeSystem
    class_class_curie: ClassVar[str] = "fhir:CodeSystem"
    class_name: ClassVar[str] = "CodeSystem"
    class_model_uri: ClassVar[URIRef] = FHIR.CodeSystem

    id: Optional[str] = None
    resourceType: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    identifier: Optional[Union[str, List[str]]] = empty_list()
    version: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    experimental: Optional[Union[bool, Bool]] = None
    date: Optional[Union[str, XSDDateTime]] = None
    publisher: Optional[str] = None
    contact: Optional[Union[str, List[str]]] = empty_list()
    description: Optional[str] = None
    filter: Optional[
        Union[Union[dict, "CodeSystemFilter"], List[Union[dict, "CodeSystemFilter"]]]
    ] = empty_list()
    property: Optional[
        Union[Union[dict, "CodeSystemProperty"], List[Union[dict, "CodeSystemProperty"]]]
    ] = empty_list()
    concept: Optional[Union[Union[dict, "Concept"], List[Union[dict, "Concept"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        if self.resourceType is not None and not isinstance(self.resourceType, str):
            self.resourceType = str(self.resourceType)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if not isinstance(self.identifier, list):
            self.identifier = [self.identifier] if self.identifier is not None else []
        self.identifier = [v if isinstance(v, str) else str(v) for v in self.identifier]

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)

        if self.status is not None and not isinstance(self.status, str):
            self.status = str(self.status)

        if self.experimental is not None and not isinstance(self.experimental, Bool):
            self.experimental = Bool(self.experimental)

        if self.date is not None and not isinstance(self.date, XSDDateTime):
            self.date = XSDDateTime(self.date)

        if self.publisher is not None and not isinstance(self.publisher, str):
            self.publisher = str(self.publisher)

        if not isinstance(self.contact, list):
            self.contact = [self.contact] if self.contact is not None else []
        self.contact = [v if isinstance(v, str) else str(v) for v in self.contact]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.filter, list):
            self.filter = [self.filter] if self.filter is not None else []
        self.filter = [
            v if isinstance(v, CodeSystemFilter) else CodeSystemFilter(**as_dict(v))
            for v in self.filter
        ]

        if not isinstance(self.property, list):
            self.property = [self.property] if self.property is not None else []
        self.property = [
            v if isinstance(v, CodeSystemProperty) else CodeSystemProperty(**as_dict(v))
            for v in self.property
        ]

        if not isinstance(self.concept, list):
            self.concept = [self.concept] if self.concept is not None else []
        self.concept = [
            v if isinstance(v, Concept) else Concept(**as_dict(v)) for v in self.concept
        ]

        super().__post_init__(**kwargs)


@dataclass
class Concept(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FHIR.Concept
    class_class_curie: ClassVar[str] = "fhir:Concept"
    class_name: ClassVar[str] = "Concept"
    class_model_uri: ClassVar[URIRef] = FHIR.Concept

    code: Optional[str] = None
    display: Optional[str] = None
    definition: Optional[str] = None
    designation: Optional[
        Union[Union[dict, "ConceptDesignation"], List[Union[dict, "ConceptDesignation"]]]
    ] = empty_list()
    property: Optional[
        Union[Union[dict, "ConceptProperty"], List[Union[dict, "ConceptProperty"]]]
    ] = empty_list()
    concept: Optional[Union[Union[dict, "Concept"], List[Union[dict, "Concept"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.code is not None and not isinstance(self.code, str):
            self.code = str(self.code)

        if self.display is not None and not isinstance(self.display, str):
            self.display = str(self.display)

        if self.definition is not None and not isinstance(self.definition, str):
            self.definition = str(self.definition)

        if not isinstance(self.designation, list):
            self.designation = [self.designation] if self.designation is not None else []
        self.designation = [
            v if isinstance(v, ConceptDesignation) else ConceptDesignation(**as_dict(v))
            for v in self.designation
        ]

        if not isinstance(self.property, list):
            self.property = [self.property] if self.property is not None else []
        self.property = [
            v if isinstance(v, ConceptProperty) else ConceptProperty(**as_dict(v))
            for v in self.property
        ]

        if not isinstance(self.concept, list):
            self.concept = [self.concept] if self.concept is not None else []
        self.concept = [
            v if isinstance(v, Concept) else Concept(**as_dict(v)) for v in self.concept
        ]

        super().__post_init__(**kwargs)


@dataclass
class ConceptProperty(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FHIR.ConceptProperty
    class_class_curie: ClassVar[str] = "fhir:ConceptProperty"
    class_name: ClassVar[str] = "ConceptProperty"
    class_model_uri: ClassVar[URIRef] = FHIR.ConceptProperty

    code: Optional[str] = None
    valueCode: Optional[str] = None
    valueCoding: Optional[str] = None
    valueString: Optional[str] = None
    valueInteger: Optional[str] = None
    valueBoolean: Optional[str] = None
    valueDateTime: Optional[str] = None
    valueDecimal: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.code is not None and not isinstance(self.code, str):
            self.code = str(self.code)

        if self.valueCode is not None and not isinstance(self.valueCode, str):
            self.valueCode = str(self.valueCode)

        if self.valueCoding is not None and not isinstance(self.valueCoding, str):
            self.valueCoding = str(self.valueCoding)

        if self.valueString is not None and not isinstance(self.valueString, str):
            self.valueString = str(self.valueString)

        if self.valueInteger is not None and not isinstance(self.valueInteger, str):
            self.valueInteger = str(self.valueInteger)

        if self.valueBoolean is not None and not isinstance(self.valueBoolean, str):
            self.valueBoolean = str(self.valueBoolean)

        if self.valueDateTime is not None and not isinstance(self.valueDateTime, str):
            self.valueDateTime = str(self.valueDateTime)

        if self.valueDecimal is not None and not isinstance(self.valueDecimal, str):
            self.valueDecimal = str(self.valueDecimal)

        super().__post_init__(**kwargs)


@dataclass
class ConceptDesignation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FHIR.ConceptDesignation
    class_class_curie: ClassVar[str] = "fhir:ConceptDesignation"
    class_name: ClassVar[str] = "ConceptDesignation"
    class_model_uri: ClassVar[URIRef] = FHIR.ConceptDesignation

    language: Optional[str] = None
    use: Optional[Union[dict, "Coding"]] = None
    value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.language is not None and not isinstance(self.language, str):
            self.language = str(self.language)

        if self.use is not None and not isinstance(self.use, Coding):
            self.use = Coding(**as_dict(self.use))

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass
class CodeSystemFilter(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FHIR.CodeSystemFilter
    class_class_curie: ClassVar[str] = "fhir:CodeSystemFilter"
    class_name: ClassVar[str] = "CodeSystemFilter"
    class_model_uri: ClassVar[URIRef] = FHIR.CodeSystemFilter

    code: str = None
    value: str = None
    description: Optional[str] = None
    operator: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.code):
            self.MissingRequiredField("code")
        if not isinstance(self.code, str):
            self.code = str(self.code)

        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.operator, list):
            self.operator = [self.operator] if self.operator is not None else []
        self.operator = [v if isinstance(v, str) else str(v) for v in self.operator]

        super().__post_init__(**kwargs)


@dataclass
class CodeSystemProperty(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FHIR.CodeSystemProperty
    class_class_curie: ClassVar[str] = "fhir:CodeSystemProperty"
    class_name: ClassVar[str] = "CodeSystemProperty"
    class_model_uri: ClassVar[URIRef] = FHIR.CodeSystemProperty

    code: str = None
    uri: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.code):
            self.MissingRequiredField("code")
        if not isinstance(self.code, str):
            self.code = str(self.code)

        if self.uri is not None and not isinstance(self.uri, str):
            self.uri = str(self.uri)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass
class Coding(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = FHIR.Coding
    class_class_curie: ClassVar[str] = "fhir:Coding"
    class_name: ClassVar[str] = "Coding"
    class_model_uri: ClassVar[URIRef] = FHIR.Coding

    system: Optional[Union[str, URI]] = None
    version: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None
    userSelected: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.system is not None and not isinstance(self.system, URI):
            self.system = URI(self.system)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.code is not None and not isinstance(self.code, str):
            self.code = str(self.code)

        if self.display is not None and not isinstance(self.display, str):
            self.display = str(self.display)

        if self.userSelected is not None and not isinstance(self.userSelected, str):
            self.userSelected = str(self.userSelected)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.codeSystem__id = Slot(
    uri=FHIR.id,
    name="codeSystem__id",
    curie=FHIR.curie("id"),
    model_uri=FHIR.codeSystem__id,
    domain=None,
    range=Optional[str],
)

slots.codeSystem__resourceType = Slot(
    uri=FHIR.resourceType,
    name="codeSystem__resourceType",
    curie=FHIR.curie("resourceType"),
    model_uri=FHIR.codeSystem__resourceType,
    domain=None,
    range=Optional[str],
)

slots.codeSystem__url = Slot(
    uri=FHIR.url,
    name="codeSystem__url",
    curie=FHIR.curie("url"),
    model_uri=FHIR.codeSystem__url,
    domain=None,
    range=Optional[Union[str, URI]],
)

slots.codeSystem__identifier = Slot(
    uri=FHIR.identifier,
    name="codeSystem__identifier",
    curie=FHIR.curie("identifier"),
    model_uri=FHIR.codeSystem__identifier,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.codeSystem__version = Slot(
    uri=FHIR.version,
    name="codeSystem__version",
    curie=FHIR.curie("version"),
    model_uri=FHIR.codeSystem__version,
    domain=None,
    range=Optional[str],
)

slots.codeSystem__name = Slot(
    uri=FHIR.name,
    name="codeSystem__name",
    curie=FHIR.curie("name"),
    model_uri=FHIR.codeSystem__name,
    domain=None,
    range=Optional[str],
)

slots.codeSystem__title = Slot(
    uri=FHIR.title,
    name="codeSystem__title",
    curie=FHIR.curie("title"),
    model_uri=FHIR.codeSystem__title,
    domain=None,
    range=Optional[str],
)

slots.codeSystem__status = Slot(
    uri=FHIR.status,
    name="codeSystem__status",
    curie=FHIR.curie("status"),
    model_uri=FHIR.codeSystem__status,
    domain=None,
    range=Optional[str],
)

slots.codeSystem__experimental = Slot(
    uri=FHIR.experimental,
    name="codeSystem__experimental",
    curie=FHIR.curie("experimental"),
    model_uri=FHIR.codeSystem__experimental,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.codeSystem__date = Slot(
    uri=FHIR.date,
    name="codeSystem__date",
    curie=FHIR.curie("date"),
    model_uri=FHIR.codeSystem__date,
    domain=None,
    range=Optional[Union[str, XSDDateTime]],
)

slots.codeSystem__publisher = Slot(
    uri=FHIR.publisher,
    name="codeSystem__publisher",
    curie=FHIR.curie("publisher"),
    model_uri=FHIR.codeSystem__publisher,
    domain=None,
    range=Optional[str],
)

slots.codeSystem__contact = Slot(
    uri=FHIR.contact,
    name="codeSystem__contact",
    curie=FHIR.curie("contact"),
    model_uri=FHIR.codeSystem__contact,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.codeSystem__description = Slot(
    uri=FHIR.description,
    name="codeSystem__description",
    curie=FHIR.curie("description"),
    model_uri=FHIR.codeSystem__description,
    domain=None,
    range=Optional[str],
)

slots.codeSystem__filter = Slot(
    uri=FHIR.filter,
    name="codeSystem__filter",
    curie=FHIR.curie("filter"),
    model_uri=FHIR.codeSystem__filter,
    domain=None,
    range=Optional[Union[Union[dict, CodeSystemFilter], List[Union[dict, CodeSystemFilter]]]],
)

slots.codeSystem__property = Slot(
    uri=FHIR.property,
    name="codeSystem__property",
    curie=FHIR.curie("property"),
    model_uri=FHIR.codeSystem__property,
    domain=None,
    range=Optional[Union[Union[dict, CodeSystemProperty], List[Union[dict, CodeSystemProperty]]]],
)

slots.codeSystem__concept = Slot(
    uri=FHIR.concept,
    name="codeSystem__concept",
    curie=FHIR.curie("concept"),
    model_uri=FHIR.codeSystem__concept,
    domain=None,
    range=Optional[Union[Union[dict, Concept], List[Union[dict, Concept]]]],
)

slots.concept__code = Slot(
    uri=FHIR.code,
    name="concept__code",
    curie=FHIR.curie("code"),
    model_uri=FHIR.concept__code,
    domain=None,
    range=Optional[str],
)

slots.concept__display = Slot(
    uri=FHIR.display,
    name="concept__display",
    curie=FHIR.curie("display"),
    model_uri=FHIR.concept__display,
    domain=None,
    range=Optional[str],
)

slots.concept__definition = Slot(
    uri=FHIR.definition,
    name="concept__definition",
    curie=FHIR.curie("definition"),
    model_uri=FHIR.concept__definition,
    domain=None,
    range=Optional[str],
)

slots.concept__designation = Slot(
    uri=FHIR.designation,
    name="concept__designation",
    curie=FHIR.curie("designation"),
    model_uri=FHIR.concept__designation,
    domain=None,
    range=Optional[Union[Union[dict, ConceptDesignation], List[Union[dict, ConceptDesignation]]]],
)

slots.concept__property = Slot(
    uri=FHIR.property,
    name="concept__property",
    curie=FHIR.curie("property"),
    model_uri=FHIR.concept__property,
    domain=None,
    range=Optional[Union[Union[dict, ConceptProperty], List[Union[dict, ConceptProperty]]]],
)

slots.concept__concept = Slot(
    uri=FHIR.concept,
    name="concept__concept",
    curie=FHIR.curie("concept"),
    model_uri=FHIR.concept__concept,
    domain=None,
    range=Optional[Union[Union[dict, Concept], List[Union[dict, Concept]]]],
)

slots.conceptProperty__code = Slot(
    uri=FHIR.code,
    name="conceptProperty__code",
    curie=FHIR.curie("code"),
    model_uri=FHIR.conceptProperty__code,
    domain=None,
    range=Optional[str],
)

slots.conceptProperty__valueCode = Slot(
    uri=FHIR.valueCode,
    name="conceptProperty__valueCode",
    curie=FHIR.curie("valueCode"),
    model_uri=FHIR.conceptProperty__valueCode,
    domain=None,
    range=Optional[str],
)

slots.conceptProperty__valueCoding = Slot(
    uri=FHIR.valueCoding,
    name="conceptProperty__valueCoding",
    curie=FHIR.curie("valueCoding"),
    model_uri=FHIR.conceptProperty__valueCoding,
    domain=None,
    range=Optional[str],
)

slots.conceptProperty__valueString = Slot(
    uri=FHIR.valueString,
    name="conceptProperty__valueString",
    curie=FHIR.curie("valueString"),
    model_uri=FHIR.conceptProperty__valueString,
    domain=None,
    range=Optional[str],
)

slots.conceptProperty__valueInteger = Slot(
    uri=FHIR.valueInteger,
    name="conceptProperty__valueInteger",
    curie=FHIR.curie("valueInteger"),
    model_uri=FHIR.conceptProperty__valueInteger,
    domain=None,
    range=Optional[str],
)

slots.conceptProperty__valueBoolean = Slot(
    uri=FHIR.valueBoolean,
    name="conceptProperty__valueBoolean",
    curie=FHIR.curie("valueBoolean"),
    model_uri=FHIR.conceptProperty__valueBoolean,
    domain=None,
    range=Optional[str],
)

slots.conceptProperty__valueDateTime = Slot(
    uri=FHIR.valueDateTime,
    name="conceptProperty__valueDateTime",
    curie=FHIR.curie("valueDateTime"),
    model_uri=FHIR.conceptProperty__valueDateTime,
    domain=None,
    range=Optional[str],
)

slots.conceptProperty__valueDecimal = Slot(
    uri=FHIR.valueDecimal,
    name="conceptProperty__valueDecimal",
    curie=FHIR.curie("valueDecimal"),
    model_uri=FHIR.conceptProperty__valueDecimal,
    domain=None,
    range=Optional[str],
)

slots.conceptDesignation__language = Slot(
    uri=FHIR.language,
    name="conceptDesignation__language",
    curie=FHIR.curie("language"),
    model_uri=FHIR.conceptDesignation__language,
    domain=None,
    range=Optional[str],
)

slots.conceptDesignation__use = Slot(
    uri=FHIR.use,
    name="conceptDesignation__use",
    curie=FHIR.curie("use"),
    model_uri=FHIR.conceptDesignation__use,
    domain=None,
    range=Optional[Union[dict, Coding]],
)

slots.conceptDesignation__value = Slot(
    uri=FHIR.value,
    name="conceptDesignation__value",
    curie=FHIR.curie("value"),
    model_uri=FHIR.conceptDesignation__value,
    domain=None,
    range=Optional[str],
)

slots.codeSystemFilter__code = Slot(
    uri=FHIR.code,
    name="codeSystemFilter__code",
    curie=FHIR.curie("code"),
    model_uri=FHIR.codeSystemFilter__code,
    domain=None,
    range=str,
)

slots.codeSystemFilter__description = Slot(
    uri=FHIR.description,
    name="codeSystemFilter__description",
    curie=FHIR.curie("description"),
    model_uri=FHIR.codeSystemFilter__description,
    domain=None,
    range=Optional[str],
)

slots.codeSystemFilter__operator = Slot(
    uri=FHIR.operator,
    name="codeSystemFilter__operator",
    curie=FHIR.curie("operator"),
    model_uri=FHIR.codeSystemFilter__operator,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.codeSystemFilter__value = Slot(
    uri=FHIR.value,
    name="codeSystemFilter__value",
    curie=FHIR.curie("value"),
    model_uri=FHIR.codeSystemFilter__value,
    domain=None,
    range=str,
)

slots.codeSystemProperty__code = Slot(
    uri=FHIR.code,
    name="codeSystemProperty__code",
    curie=FHIR.curie("code"),
    model_uri=FHIR.codeSystemProperty__code,
    domain=None,
    range=str,
)

slots.codeSystemProperty__uri = Slot(
    uri=FHIR.uri,
    name="codeSystemProperty__uri",
    curie=FHIR.curie("uri"),
    model_uri=FHIR.codeSystemProperty__uri,
    domain=None,
    range=Optional[str],
)

slots.codeSystemProperty__description = Slot(
    uri=FHIR.description,
    name="codeSystemProperty__description",
    curie=FHIR.curie("description"),
    model_uri=FHIR.codeSystemProperty__description,
    domain=None,
    range=Optional[str],
)

slots.codeSystemProperty__type = Slot(
    uri=FHIR.type,
    name="codeSystemProperty__type",
    curie=FHIR.curie("type"),
    model_uri=FHIR.codeSystemProperty__type,
    domain=None,
    range=Optional[str],
)

slots.coding__system = Slot(
    uri=FHIR.system,
    name="coding__system",
    curie=FHIR.curie("system"),
    model_uri=FHIR.coding__system,
    domain=None,
    range=Optional[Union[str, URI]],
)

slots.coding__version = Slot(
    uri=FHIR.version,
    name="coding__version",
    curie=FHIR.curie("version"),
    model_uri=FHIR.coding__version,
    domain=None,
    range=Optional[str],
)

slots.coding__code = Slot(
    uri=FHIR.code,
    name="coding__code",
    curie=FHIR.curie("code"),
    model_uri=FHIR.coding__code,
    domain=None,
    range=Optional[str],
)

slots.coding__display = Slot(
    uri=FHIR.display,
    name="coding__display",
    curie=FHIR.curie("display"),
    model_uri=FHIR.coding__display,
    domain=None,
    range=Optional[str],
)

slots.coding__userSelected = Slot(
    uri=FHIR.userSelected,
    name="coding__userSelected",
    curie=FHIR.curie("userSelected"),
    model_uri=FHIR.coding__userSelected,
    domain=None,
    range=Optional[str],
)
