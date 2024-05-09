# Auto generated from validation_datamodel.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-04-14T16:59:08
# Schema: validaton-results
#
# id: https://w3id.org/linkml/validation_results
# description: A datamodel for data validation results.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from datetime import date, datetime
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Float, Integer, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE

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
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SH = CurieNamespace('sh', 'http://www.w3.org/ns/shacl#')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
VM = CurieNamespace('vm', 'https://w3id.org/linkml/validation-model/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = VM


# Types

# Class references
class NamedResourceId(URIorCURIE):
    pass


class ConstraintComponentId(NamedResourceId):
    pass


class NodeId(NamedResourceId):
    pass


class TypeSeverityKeyValueType(URIorCURIE):
    pass


@dataclass
class NamedResource(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["NamedResource"]
    class_class_curie: ClassVar[str] = "vm:NamedResource"
    class_name: ClassVar[str] = "NamedResource"
    class_model_uri: ClassVar[URIRef] = VM.NamedResource

    id: Union[str, NamedResourceId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedResourceId):
            self.id = NamedResourceId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ConstraintComponent(NamedResource):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["ConstraintComponent"]
    class_class_curie: ClassVar[str] = "vm:ConstraintComponent"
    class_name: ClassVar[str] = "ConstraintComponent"
    class_model_uri: ClassVar[URIRef] = VM.ConstraintComponent

    id: Union[str, ConstraintComponentId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConstraintComponentId):
            self.id = ConstraintComponentId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Node(NamedResource):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["Node"]
    class_class_curie: ClassVar[str] = "vm:Node"
    class_name: ClassVar[str] = "Node"
    class_model_uri: ClassVar[URIRef] = VM.Node

    id: Union[str, NodeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeId):
            self.id = NodeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ValidationConfiguration(YAMLRoot):
    """
    Configuration parameters for execution of a validation report
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["ValidationConfiguration"]
    class_class_curie: ClassVar[str] = "vm:ValidationConfiguration"
    class_name: ClassVar[str] = "ValidationConfiguration"
    class_model_uri: ClassVar[URIRef] = VM.ValidationConfiguration

    max_number_results_per_type: Optional[int] = None
    type_severity_map: Optional[Union[Dict[Union[str, TypeSeverityKeyValueType], Union[dict, "TypeSeverityKeyValue"]], List[Union[dict, "TypeSeverityKeyValue"]]]] = empty_dict()
    schema_path: Optional[str] = None
    lookup_references: Optional[Union[bool, Bool]] = None
    prompt_info: Optional[str] = None
    documentation_objects: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.max_number_results_per_type is not None and not isinstance(self.max_number_results_per_type, int):
            self.max_number_results_per_type = int(self.max_number_results_per_type)

        self._normalize_inlined_as_dict(slot_name="type_severity_map", slot_type=TypeSeverityKeyValue, key_name="type", keyed=True)

        if self.schema_path is not None and not isinstance(self.schema_path, str):
            self.schema_path = str(self.schema_path)

        if self.lookup_references is not None and not isinstance(self.lookup_references, Bool):
            self.lookup_references = Bool(self.lookup_references)

        if self.prompt_info is not None and not isinstance(self.prompt_info, str):
            self.prompt_info = str(self.prompt_info)

        if not isinstance(self.documentation_objects, list):
            self.documentation_objects = [self.documentation_objects] if self.documentation_objects is not None else []
        self.documentation_objects = [v if isinstance(v, str) else str(v) for v in self.documentation_objects]

        super().__post_init__(**kwargs)


@dataclass
class RepairConfiguration(YAMLRoot):
    """
    Configuration parameters for execution of validation repairs
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["RepairConfiguration"]
    class_class_curie: ClassVar[str] = "vm:RepairConfiguration"
    class_name: ClassVar[str] = "RepairConfiguration"
    class_model_uri: ClassVar[URIRef] = VM.RepairConfiguration

    validation_configuration: Optional[Union[dict, ValidationConfiguration]] = None
    dry_run: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.validation_configuration is not None and not isinstance(self.validation_configuration, ValidationConfiguration):
            self.validation_configuration = ValidationConfiguration(**as_dict(self.validation_configuration))

        if self.dry_run is not None and not isinstance(self.dry_run, Bool):
            self.dry_run = Bool(self.dry_run)

        super().__post_init__(**kwargs)


@dataclass
class TypeSeverityKeyValue(YAMLRoot):
    """
    key-value pair that maps a validation result type to a severity setting, for overriding default severity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["TypeSeverityKeyValue"]
    class_class_curie: ClassVar[str] = "vm:TypeSeverityKeyValue"
    class_name: ClassVar[str] = "TypeSeverityKeyValue"
    class_model_uri: ClassVar[URIRef] = VM.TypeSeverityKeyValue

    type: Union[str, TypeSeverityKeyValueType] = None
    severity: Optional[Union[str, "SeverityOptions"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, TypeSeverityKeyValueType):
            self.type = TypeSeverityKeyValueType(self.type)

        if self.severity is not None and not isinstance(self.severity, SeverityOptions):
            self.severity = SeverityOptions(self.severity)

        super().__post_init__(**kwargs)


@dataclass
class Report(YAMLRoot):
    """
    A report object that is a holder to multiple report results
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["Report"]
    class_class_curie: ClassVar[str] = "vm:Report"
    class_name: ClassVar[str] = "Report"
    class_model_uri: ClassVar[URIRef] = VM.Report

    results: Optional[Union[Union[dict, "Result"], List[Union[dict, "Result"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, Result) else Result(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


@dataclass
class ValidationReport(Report):
    """
    A report that consists of validation results
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH["ValidationReport"]
    class_class_curie: ClassVar[str] = "sh:ValidationReport"
    class_name: ClassVar[str] = "ValidationReport"
    class_model_uri: ClassVar[URIRef] = VM.ValidationReport

    results: Optional[Union[Union[dict, "ValidationResult"], List[Union[dict, "ValidationResult"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, ValidationResult) else ValidationResult(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


@dataclass
class RepairReport(Report):
    """
    A report that consists of repair operation results
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["RepairReport"]
    class_class_curie: ClassVar[str] = "vm:RepairReport"
    class_name: ClassVar[str] = "RepairReport"
    class_model_uri: ClassVar[URIRef] = VM.RepairReport

    results: Optional[Union[Union[dict, "RepairOperation"], List[Union[dict, "RepairOperation"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [v if isinstance(v, RepairOperation) else RepairOperation(**as_dict(v)) for v in self.results]

        super().__post_init__(**kwargs)


class Result(YAMLRoot):
    """
    Abstract base class for any individual report result
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["Result"]
    class_class_curie: ClassVar[str] = "vm:Result"
    class_name: ClassVar[str] = "Result"
    class_model_uri: ClassVar[URIRef] = VM.Result


@dataclass
class ValidationResult(Result):
    """
    An individual result arising from validation of a data instance using a particular rule
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH["ValidationResult"]
    class_class_curie: ClassVar[str] = "sh:ValidationResult"
    class_name: ClassVar[str] = "ValidationResult"
    class_model_uri: ClassVar[URIRef] = VM.ValidationResult

    type: Union[str, ConstraintComponentId] = None
    subject: Union[str, NodeId] = None
    severity: Optional[Union[str, "SeverityOptions"]] = None
    instantiates: Optional[Union[str, NodeId]] = None
    predicate: Optional[Union[str, NodeId]] = None
    object: Optional[Union[str, NodeId]] = None
    object_str: Optional[str] = None
    source: Optional[str] = None
    info: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, ConstraintComponentId):
            self.type = ConstraintComponentId(self.type)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, NodeId):
            self.subject = NodeId(self.subject)

        if self.severity is not None and not isinstance(self.severity, SeverityOptions):
            self.severity = SeverityOptions(self.severity)

        if self.instantiates is not None and not isinstance(self.instantiates, NodeId):
            self.instantiates = NodeId(self.instantiates)

        if self.predicate is not None and not isinstance(self.predicate, NodeId):
            self.predicate = NodeId(self.predicate)

        if self.object is not None and not isinstance(self.object, NodeId):
            self.object = NodeId(self.object)

        if self.object_str is not None and not isinstance(self.object_str, str):
            self.object_str = str(self.object_str)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        super().__post_init__(**kwargs)


@dataclass
class DefinitionValidationResult(ValidationResult):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["DefinitionValidationResult"]
    class_class_curie: ClassVar[str] = "vm:DefinitionValidationResult"
    class_name: ClassVar[str] = "DefinitionValidationResult"
    class_model_uri: ClassVar[URIRef] = VM.DefinitionValidationResult

    type: Union[str, ConstraintComponentId] = None
    subject: Union[str, NodeId] = None
    definition: Optional[str] = None
    definition_source: Optional[str] = None
    proposed_new_definition: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.definition is not None and not isinstance(self.definition, str):
            self.definition = str(self.definition)

        if self.definition_source is not None and not isinstance(self.definition_source, str):
            self.definition_source = str(self.definition_source)

        if self.proposed_new_definition is not None and not isinstance(self.proposed_new_definition, str):
            self.proposed_new_definition = str(self.proposed_new_definition)

        super().__post_init__(**kwargs)


@dataclass
class MappingValidationResult(Result):
    """
    A validation result where the check is to determine if a mapping is correct
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["MappingValidationResult"]
    class_class_curie: ClassVar[str] = "vm:MappingValidationResult"
    class_name: ClassVar[str] = "MappingValidationResult"
    class_model_uri: ClassVar[URIRef] = VM.MappingValidationResult

    subject_id: Optional[str] = None
    subject_info: Optional[str] = None
    object_id: Optional[str] = None
    object_info: Optional[str] = None
    predicate_id: Optional[str] = None
    category: Optional[str] = None
    problem: Optional[Union[bool, Bool]] = None
    info: Optional[str] = None
    confidence: Optional[float] = None
    suggested_predicate: Optional[str] = None
    suggested_modifications: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject_id is not None and not isinstance(self.subject_id, str):
            self.subject_id = str(self.subject_id)

        if self.subject_info is not None and not isinstance(self.subject_info, str):
            self.subject_info = str(self.subject_info)

        if self.object_id is not None and not isinstance(self.object_id, str):
            self.object_id = str(self.object_id)

        if self.object_info is not None and not isinstance(self.object_info, str):
            self.object_info = str(self.object_info)

        if self.predicate_id is not None and not isinstance(self.predicate_id, str):
            self.predicate_id = str(self.predicate_id)

        if self.category is not None and not isinstance(self.category, str):
            self.category = str(self.category)

        if self.problem is not None and not isinstance(self.problem, Bool):
            self.problem = Bool(self.problem)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        if self.confidence is not None and not isinstance(self.confidence, float):
            self.confidence = float(self.confidence)

        if self.suggested_predicate is not None and not isinstance(self.suggested_predicate, str):
            self.suggested_predicate = str(self.suggested_predicate)

        if self.suggested_modifications is not None and not isinstance(self.suggested_modifications, str):
            self.suggested_modifications = str(self.suggested_modifications)

        super().__post_init__(**kwargs)


@dataclass
class RepairOperation(Result):
    """
    The result of performing an individual repair
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["RepairOperation"]
    class_class_curie: ClassVar[str] = "vm:RepairOperation"
    class_name: ClassVar[str] = "RepairOperation"
    class_model_uri: ClassVar[URIRef] = VM.RepairOperation

    repairs: Optional[Union[dict, ValidationResult]] = None
    modified: Optional[Union[bool, Bool]] = None
    successful: Optional[Union[bool, Bool]] = None
    info: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.repairs is not None and not isinstance(self.repairs, ValidationResult):
            self.repairs = ValidationResult(**as_dict(self.repairs))

        if self.modified is not None and not isinstance(self.modified, Bool):
            self.modified = Bool(self.modified)

        if self.successful is not None and not isinstance(self.successful, Bool):
            self.successful = Bool(self.successful)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        super().__post_init__(**kwargs)


@dataclass
class ExternalReferenceValidationResult(ValidationResult):
    """
    A validation result where the check is to determine if a link to an external resource is still valid
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM["ExternalReferenceValidationResult"]
    class_class_curie: ClassVar[str] = "vm:ExternalReferenceValidationResult"
    class_name: ClassVar[str] = "ExternalReferenceValidationResult"
    class_model_uri: ClassVar[URIRef] = VM.ExternalReferenceValidationResult

    type: Union[str, ConstraintComponentId] = None
    subject: Union[str, NodeId] = None
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
    ERROR = PermissibleValue(
        text="ERROR",
        meaning=SH["Violation"])
    WARNING = PermissibleValue(
        text="WARNING",
        meaning=SH["Warning"])
    INFO = PermissibleValue(
        text="INFO",
        meaning=SH["Info"])

    _defn = EnumDefinition(
        name="SeverityOptions",
    )

class ValidationResultType(EnumDefinitionImpl):

    DatatypeConstraintComponent = PermissibleValue(
        text="DatatypeConstraintComponent",
        description="constraint in which the range is a type, and the slot value must conform to the type",
        meaning=SH["DatatypeConstraintComponent"])
    MinCountConstraintComponent = PermissibleValue(
        text="MinCountConstraintComponent",
        description="cardinality constraint where the slot value must be greater or equal to a specified minimum",
        meaning=SH["MinCountConstraintComponent"])
    MaxCountConstraintComponent = PermissibleValue(
        text="MaxCountConstraintComponent",
        description="cardinality constraint where the slot value must be less than or equal to a specified maximum",
        meaning=SH["MaxCountConstraintComponent"])
    DeprecatedPropertyComponent = PermissibleValue(
        text="DeprecatedPropertyComponent",
        description="constraint where the instance slot should not be deprecated",
        meaning=VM["DeprecatedPropertyComponent"])
    MaxLengthConstraintComponent = PermissibleValue(
        text="MaxLengthConstraintComponent",
        description="constraint where the slot value must have a length equal to or less than a specified maximum",
        meaning=SH["MaxLengthConstraintComponent"])
    MinLengthConstraintComponent = PermissibleValue(
        text="MinLengthConstraintComponent",
        description="constraint where the slot value must have a length equal to or less than a specified maximum",
        meaning=SH["MinLengthConstraintComponent"])
    PatternConstraintComponent = PermissibleValue(
        text="PatternConstraintComponent",
        description="constraint where the slot value must match a given regular expression pattern",
        meaning=SH["PatternConstraintComponent"])
    ClosedConstraintComponent = PermissibleValue(
        text="ClosedConstraintComponent",
        description="constraint where the slot value must be allowable for the type of an instance",
        meaning=SH["ClosedConstraintComponent"])
    RuleConstraintComponent = PermissibleValue(
        text="RuleConstraintComponent",
        description="constraint where the structure of an object must conform to a specified rule")

    _defn = EnumDefinition(
        name="ValidationResultType",
    )

# Slots
class slots:
    pass

slots.type = Slot(uri=SH.sourceConstraintComponent, name="type", curie=SH.curie('sourceConstraintComponent'),
                   model_uri=VM.type, domain=None, range=Union[str, ConstraintComponentId])

slots.subject = Slot(uri=SH.focusNode, name="subject", curie=SH.curie('focusNode'),
                   model_uri=VM.subject, domain=None, range=Union[str, NodeId])

slots.instantiates = Slot(uri=VM.instantiates, name="instantiates", curie=VM.curie('instantiates'),
                   model_uri=VM.instantiates, domain=None, range=Optional[Union[str, NodeId]])

slots.predicate = Slot(uri=VM.predicate, name="predicate", curie=VM.curie('predicate'),
                   model_uri=VM.predicate, domain=None, range=Optional[Union[str, NodeId]])

slots.object = Slot(uri=SH.value, name="object", curie=SH.curie('value'),
                   model_uri=VM.object, domain=None, range=Optional[Union[str, NodeId]])

slots.object_str = Slot(uri=VM.object_str, name="object_str", curie=VM.curie('object_str'),
                   model_uri=VM.object_str, domain=None, range=Optional[str])

slots.source = Slot(uri=VM.source, name="source", curie=VM.curie('source'),
                   model_uri=VM.source, domain=None, range=Optional[str])

slots.severity = Slot(uri=SH.resultSeverity, name="severity", curie=SH.curie('resultSeverity'),
                   model_uri=VM.severity, domain=None, range=Optional[Union[str, "SeverityOptions"]])

slots.info = Slot(uri=SH.resultMessage, name="info", curie=SH.curie('resultMessage'),
                   model_uri=VM.info, domain=None, range=Optional[str])

slots.results = Slot(uri=SH.result, name="results", curie=SH.curie('result'),
                   model_uri=VM.results, domain=None, range=Optional[Union[Union[dict, Result], List[Union[dict, Result]]]])

slots.namedResource__id = Slot(uri=VM.id, name="namedResource__id", curie=VM.curie('id'),
                   model_uri=VM.namedResource__id, domain=None, range=URIRef)

slots.validationConfiguration__max_number_results_per_type = Slot(uri=VM.max_number_results_per_type, name="validationConfiguration__max_number_results_per_type", curie=VM.curie('max_number_results_per_type'),
                   model_uri=VM.validationConfiguration__max_number_results_per_type, domain=None, range=Optional[int])

slots.validationConfiguration__type_severity_map = Slot(uri=VM.type_severity_map, name="validationConfiguration__type_severity_map", curie=VM.curie('type_severity_map'),
                   model_uri=VM.validationConfiguration__type_severity_map, domain=None, range=Optional[Union[Dict[Union[str, TypeSeverityKeyValueType], Union[dict, TypeSeverityKeyValue]], List[Union[dict, TypeSeverityKeyValue]]]])

slots.validationConfiguration__schema_path = Slot(uri=VM.schema_path, name="validationConfiguration__schema_path", curie=VM.curie('schema_path'),
                   model_uri=VM.validationConfiguration__schema_path, domain=None, range=Optional[str])

slots.validationConfiguration__lookup_references = Slot(uri=VM.lookup_references, name="validationConfiguration__lookup_references", curie=VM.curie('lookup_references'),
                   model_uri=VM.validationConfiguration__lookup_references, domain=None, range=Optional[Union[bool, Bool]])

slots.validationConfiguration__prompt_info = Slot(uri=VM.prompt_info, name="validationConfiguration__prompt_info", curie=VM.curie('prompt_info'),
                   model_uri=VM.validationConfiguration__prompt_info, domain=None, range=Optional[str])

slots.validationConfiguration__documentation_objects = Slot(uri=VM.documentation_objects, name="validationConfiguration__documentation_objects", curie=VM.curie('documentation_objects'),
                   model_uri=VM.validationConfiguration__documentation_objects, domain=None, range=Optional[Union[str, List[str]]])

slots.repairConfiguration__validation_configuration = Slot(uri=VM.validation_configuration, name="repairConfiguration__validation_configuration", curie=VM.curie('validation_configuration'),
                   model_uri=VM.repairConfiguration__validation_configuration, domain=None, range=Optional[Union[dict, ValidationConfiguration]])

slots.repairConfiguration__dry_run = Slot(uri=VM.dry_run, name="repairConfiguration__dry_run", curie=VM.curie('dry_run'),
                   model_uri=VM.repairConfiguration__dry_run, domain=None, range=Optional[Union[bool, Bool]])

slots.typeSeverityKeyValue__type = Slot(uri=VM.type, name="typeSeverityKeyValue__type", curie=VM.curie('type'),
                   model_uri=VM.typeSeverityKeyValue__type, domain=None, range=URIRef)

slots.typeSeverityKeyValue__severity = Slot(uri=VM.severity, name="typeSeverityKeyValue__severity", curie=VM.curie('severity'),
                   model_uri=VM.typeSeverityKeyValue__severity, domain=None, range=Optional[Union[str, "SeverityOptions"]])

slots.definitionValidationResult__definition = Slot(uri=VM.definition, name="definitionValidationResult__definition", curie=VM.curie('definition'),
                   model_uri=VM.definitionValidationResult__definition, domain=None, range=Optional[str])

slots.definitionValidationResult__definition_source = Slot(uri=VM.definition_source, name="definitionValidationResult__definition_source", curie=VM.curie('definition_source'),
                   model_uri=VM.definitionValidationResult__definition_source, domain=None, range=Optional[str])

slots.definitionValidationResult__proposed_new_definition = Slot(uri=VM.proposed_new_definition, name="definitionValidationResult__proposed_new_definition", curie=VM.curie('proposed_new_definition'),
                   model_uri=VM.definitionValidationResult__proposed_new_definition, domain=None, range=Optional[str])

slots.mappingValidationResult__subject_id = Slot(uri=VM.subject_id, name="mappingValidationResult__subject_id", curie=VM.curie('subject_id'),
                   model_uri=VM.mappingValidationResult__subject_id, domain=None, range=Optional[str])

slots.mappingValidationResult__subject_info = Slot(uri=VM.subject_info, name="mappingValidationResult__subject_info", curie=VM.curie('subject_info'),
                   model_uri=VM.mappingValidationResult__subject_info, domain=None, range=Optional[str])

slots.mappingValidationResult__object_id = Slot(uri=VM.object_id, name="mappingValidationResult__object_id", curie=VM.curie('object_id'),
                   model_uri=VM.mappingValidationResult__object_id, domain=None, range=Optional[str])

slots.mappingValidationResult__object_info = Slot(uri=VM.object_info, name="mappingValidationResult__object_info", curie=VM.curie('object_info'),
                   model_uri=VM.mappingValidationResult__object_info, domain=None, range=Optional[str])

slots.mappingValidationResult__predicate_id = Slot(uri=VM.predicate_id, name="mappingValidationResult__predicate_id", curie=VM.curie('predicate_id'),
                   model_uri=VM.mappingValidationResult__predicate_id, domain=None, range=Optional[str])

slots.mappingValidationResult__category = Slot(uri=VM.category, name="mappingValidationResult__category", curie=VM.curie('category'),
                   model_uri=VM.mappingValidationResult__category, domain=None, range=Optional[str])

slots.mappingValidationResult__problem = Slot(uri=VM.problem, name="mappingValidationResult__problem", curie=VM.curie('problem'),
                   model_uri=VM.mappingValidationResult__problem, domain=None, range=Optional[Union[bool, Bool]])

slots.mappingValidationResult__info = Slot(uri=VM.info, name="mappingValidationResult__info", curie=VM.curie('info'),
                   model_uri=VM.mappingValidationResult__info, domain=None, range=Optional[str])

slots.mappingValidationResult__confidence = Slot(uri=VM.confidence, name="mappingValidationResult__confidence", curie=VM.curie('confidence'),
                   model_uri=VM.mappingValidationResult__confidence, domain=None, range=Optional[float])

slots.mappingValidationResult__suggested_predicate = Slot(uri=VM.suggested_predicate, name="mappingValidationResult__suggested_predicate", curie=VM.curie('suggested_predicate'),
                   model_uri=VM.mappingValidationResult__suggested_predicate, domain=None, range=Optional[str])

slots.mappingValidationResult__suggested_modifications = Slot(uri=VM.suggested_modifications, name="mappingValidationResult__suggested_modifications", curie=VM.curie('suggested_modifications'),
                   model_uri=VM.mappingValidationResult__suggested_modifications, domain=None, range=Optional[str])

slots.repairOperation__repairs = Slot(uri=VM.repairs, name="repairOperation__repairs", curie=VM.curie('repairs'),
                   model_uri=VM.repairOperation__repairs, domain=None, range=Optional[Union[dict, ValidationResult]])

slots.repairOperation__modified = Slot(uri=VM.modified, name="repairOperation__modified", curie=VM.curie('modified'),
                   model_uri=VM.repairOperation__modified, domain=None, range=Optional[Union[bool, Bool]])

slots.repairOperation__successful = Slot(uri=VM.successful, name="repairOperation__successful", curie=VM.curie('successful'),
                   model_uri=VM.repairOperation__successful, domain=None, range=Optional[Union[bool, Bool]])

slots.repairOperation__info = Slot(uri=VM.info, name="repairOperation__info", curie=VM.curie('info'),
                   model_uri=VM.repairOperation__info, domain=None, range=Optional[str])

slots.externalReferenceValidationResult__url = Slot(uri=VM.url, name="externalReferenceValidationResult__url", curie=VM.curie('url'),
                   model_uri=VM.externalReferenceValidationResult__url, domain=None, range=Optional[str])

slots.externalReferenceValidationResult__time_checked = Slot(uri=VM.time_checked, name="externalReferenceValidationResult__time_checked", curie=VM.curie('time_checked'),
                   model_uri=VM.externalReferenceValidationResult__time_checked, domain=None, range=Optional[str])

slots.externalReferenceValidationResult__number_of_attempts = Slot(uri=VM.number_of_attempts, name="externalReferenceValidationResult__number_of_attempts", curie=VM.curie('number_of_attempts'),
                   model_uri=VM.externalReferenceValidationResult__number_of_attempts, domain=None, range=Optional[int])

slots.externalReferenceValidationResult__http_response_code = Slot(uri=VM.http_response_code, name="externalReferenceValidationResult__http_response_code", curie=VM.curie('http_response_code'),
                   model_uri=VM.externalReferenceValidationResult__http_response_code, domain=None, range=Optional[int])

slots.ValidationReport_results = Slot(uri=SH.result, name="ValidationReport_results", curie=SH.curie('result'),
                   model_uri=VM.ValidationReport_results, domain=ValidationReport, range=Optional[Union[Union[dict, "ValidationResult"], List[Union[dict, "ValidationResult"]]]])

slots.RepairReport_results = Slot(uri=SH.result, name="RepairReport_results", curie=SH.curie('result'),
                   model_uri=VM.RepairReport_results, domain=RepairReport, range=Optional[Union[Union[dict, "RepairOperation"], List[Union[dict, "RepairOperation"]]]])
