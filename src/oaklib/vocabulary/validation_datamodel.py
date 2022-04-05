# Auto generated from validation_datamodel.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-03-31T09:17:43
# Schema: validaton-results
#
# id: https://w3id.org/linkml/validation_results
# description: A datamodel for reports on data
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Integer, Nodeidentifier, String
from linkml_runtime.utils.metamodelcore import NodeIdentifier

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
REPORTING = CurieNamespace('reporting', 'https://w3id.org/linkml/report')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = REPORTING


# Types

# Class references



@dataclass
class ValidationReport(YAMLRoot):
    """
    A report object
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH.ValidationReport
    class_class_curie: ClassVar[str] = "sh:ValidationReport"
    class_name: ClassVar[str] = "ValidationReport"
    class_model_uri: ClassVar[URIRef] = REPORTING.ValidationReport

    results: Optional[Union[Union[dict, "ValidationResult"], List[Union[dict, "ValidationResult"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, ValidationResult) else ValidationResult(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


@dataclass
class ValidationResult(YAMLRoot):
    """
    An individual result arising from validation of a data instance using a particular rule
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH.ValidationResult
    class_class_curie: ClassVar[str] = "sh:ValidationResult"
    class_name: ClassVar[str] = "ValidationResult"
    class_model_uri: ClassVar[URIRef] = REPORTING.ValidationResult

    type: Optional[Union[str, NodeIdentifier]] = None
    severity: Optional[Union[str, "SeverityOptions"]] = None
    subject: Optional[Union[str, NodeIdentifier]] = None
    instantiates: Optional[Union[str, NodeIdentifier]] = None
    predicate: Optional[Union[str, NodeIdentifier]] = None
    object: Optional[Union[str, NodeIdentifier]] = None
    object_str: Optional[str] = None
    source: Optional[Union[str, NodeIdentifier]] = None
    info: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, NodeIdentifier):
            self.type = NodeIdentifier(self.type)

        if self.severity is not None and not isinstance(self.severity, SeverityOptions):
            self.severity = SeverityOptions(self.severity)

        if self.subject is not None and not isinstance(self.subject, NodeIdentifier):
            self.subject = NodeIdentifier(self.subject)

        if self.instantiates is not None and not isinstance(self.instantiates, NodeIdentifier):
            self.instantiates = NodeIdentifier(self.instantiates)

        if self.predicate is not None and not isinstance(self.predicate, NodeIdentifier):
            self.predicate = NodeIdentifier(self.predicate)

        if self.object is not None and not isinstance(self.object, NodeIdentifier):
            self.object = NodeIdentifier(self.object)

        if self.object_str is not None and not isinstance(self.object_str, str):
            self.object_str = str(self.object_str)

        if self.source is not None and not isinstance(self.source, NodeIdentifier):
            self.source = NodeIdentifier(self.source)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        super().__post_init__(**kwargs)


@dataclass
class ExternalReferenceValidationResult(ValidationResult):
    """
    A validation result where the check is to determine if a link to an external resource is still valid
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.ExternalReferenceValidationResult
    class_class_curie: ClassVar[str] = "reporting:ExternalReferenceValidationResult"
    class_name: ClassVar[str] = "ExternalReferenceValidationResult"
    class_model_uri: ClassVar[URIRef] = REPORTING.ExternalReferenceValidationResult

    url: Optional[str] = None
    time_checked: Optional[str] = None
    number_of_attempts: Optional[int] = None
    http_response_code: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.url is not None and not isinstance(self.url, str):
            self.url = str(self.url)

        if self.time_checked is not None and not isinstance(self.time_checked, str):
            self.time_checked = str(self.time_checked)

        if self.number_of_attempts is not None and not isinstance(self.number_of_attempts, int):
            self.number_of_attempts = int(self.number_of_attempts)

        if self.http_response_code is not None and not isinstance(self.http_response_code, int):
            self.http_response_code = int(self.http_response_code)

        super().__post_init__(**kwargs)


# Enumerations
class SeverityOptions(EnumDefinitionImpl):

    FATAL = PermissibleValue(text="FATAL")
    ERROR = PermissibleValue(text="ERROR",
                                 meaning=SH.Violation)
    WARNING = PermissibleValue(text="WARNING",
                                     meaning=SH.Warning)
    INFO = PermissibleValue(text="INFO",
                               meaning=SH.Info)

    _defn = EnumDefinition(
        name="SeverityOptions",
    )

# Slots
class slots:
    pass

slots.type = Slot(uri=SH.sourceConstraintComponent, name="type", curie=SH.curie('sourceConstraintComponent'),
                   model_uri=REPORTING.type, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.subject = Slot(uri=SH.focusNode, name="subject", curie=SH.curie('focusNode'),
                   model_uri=REPORTING.subject, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.instantiates = Slot(uri=REPORTING.instantiates, name="instantiates", curie=REPORTING.curie('instantiates'),
                   model_uri=REPORTING.instantiates, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.predicate = Slot(uri=REPORTING.predicate, name="predicate", curie=REPORTING.curie('predicate'),
                   model_uri=REPORTING.predicate, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.object = Slot(uri=SH.value, name="object", curie=SH.curie('value'),
                   model_uri=REPORTING.object, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.object_str = Slot(uri=REPORTING.object_str, name="object_str", curie=REPORTING.curie('object_str'),
                   model_uri=REPORTING.object_str, domain=None, range=Optional[str])

slots.source = Slot(uri=REPORTING.source, name="source", curie=REPORTING.curie('source'),
                   model_uri=REPORTING.source, domain=None, range=Optional[Union[str, NodeIdentifier]])

slots.severity = Slot(uri=REPORTING.severity, name="severity", curie=REPORTING.curie('severity'),
                   model_uri=REPORTING.severity, domain=None, range=Optional[Union[str, "SeverityOptions"]])

slots.info = Slot(uri=REPORTING.info, name="info", curie=REPORTING.curie('info'),
                   model_uri=REPORTING.info, domain=None, range=Optional[str])

slots.validationReport__results = Slot(uri=REPORTING.results, name="validationReport__results", curie=REPORTING.curie('results'),
                   model_uri=REPORTING.validationReport__results, domain=None, range=Optional[Union[Union[dict, ValidationResult], List[Union[dict, ValidationResult]]]])

slots.externalReferenceValidationResult__url = Slot(uri=REPORTING.url, name="externalReferenceValidationResult__url", curie=REPORTING.curie('url'),
                   model_uri=REPORTING.externalReferenceValidationResult__url, domain=None, range=Optional[str])

slots.externalReferenceValidationResult__time_checked = Slot(uri=REPORTING.time_checked, name="externalReferenceValidationResult__time_checked", curie=REPORTING.curie('time_checked'),
                   model_uri=REPORTING.externalReferenceValidationResult__time_checked, domain=None, range=Optional[str])

slots.externalReferenceValidationResult__number_of_attempts = Slot(uri=REPORTING.number_of_attempts, name="externalReferenceValidationResult__number_of_attempts", curie=REPORTING.curie('number_of_attempts'),
                   model_uri=REPORTING.externalReferenceValidationResult__number_of_attempts, domain=None, range=Optional[int])

slots.externalReferenceValidationResult__http_response_code = Slot(uri=REPORTING.http_response_code, name="externalReferenceValidationResult__http_response_code", curie=REPORTING.curie('http_response_code'),
                   model_uri=REPORTING.externalReferenceValidationResult__http_response_code, domain=None, range=Optional[int])
