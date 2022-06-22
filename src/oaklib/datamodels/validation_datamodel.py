# Auto generated from validation_datamodel.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-05-30T15:33:38
# Schema: validaton-results
#
# id: https://w3id.org/linkml/validation_results
# description: A datamodel for data validation results.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import as_dict
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import URIRef

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "http://www.w3.org/ns/shacl#")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
VM = CurieNamespace("vm", "https://w3id.org/linkml/validation-model/")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = VM


# Types

# Class references
class TypeSeverityKeyValueType(URIorCURIE):
    pass


@dataclass
class ValidationConfiguration(YAMLRoot):
    """
    Configuration parameters for execution of a validation report
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM.ValidationConfiguration
    class_class_curie: ClassVar[str] = "vm:ValidationConfiguration"
    class_name: ClassVar[str] = "ValidationConfiguration"
    class_model_uri: ClassVar[URIRef] = VM.ValidationConfiguration

    max_number_results_per_type: Optional[int] = None
    type_severity_map: Optional[
        Union[
            Dict[Union[str, TypeSeverityKeyValueType], Union[dict, "TypeSeverityKeyValue"]],
            List[Union[dict, "TypeSeverityKeyValue"]],
        ]
    ] = empty_dict()
    schema_path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.max_number_results_per_type is not None and not isinstance(
            self.max_number_results_per_type, int
        ):
            self.max_number_results_per_type = int(self.max_number_results_per_type)

        self._normalize_inlined_as_dict(
            slot_name="type_severity_map",
            slot_type=TypeSeverityKeyValue,
            key_name="type",
            keyed=True,
        )

        if self.schema_path is not None and not isinstance(self.schema_path, str):
            self.schema_path = str(self.schema_path)

        super().__post_init__(**kwargs)


@dataclass
class RepairConfiguration(YAMLRoot):
    """
    Configuration parameters for execution of validation repairs
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM.RepairConfiguration
    class_class_curie: ClassVar[str] = "vm:RepairConfiguration"
    class_name: ClassVar[str] = "RepairConfiguration"
    class_model_uri: ClassVar[URIRef] = VM.RepairConfiguration

    validation_configuration: Optional[Union[dict, ValidationConfiguration]] = None
    dry_run: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.validation_configuration is not None and not isinstance(
            self.validation_configuration, ValidationConfiguration
        ):
            self.validation_configuration = ValidationConfiguration(
                **as_dict(self.validation_configuration)
            )

        if self.dry_run is not None and not isinstance(self.dry_run, Bool):
            self.dry_run = Bool(self.dry_run)

        super().__post_init__(**kwargs)


@dataclass
class TypeSeverityKeyValue(YAMLRoot):
    """
    key-value pair that maps a validation result type to a severity setting, for overriding default severity
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM.TypeSeverityKeyValue
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

    class_class_uri: ClassVar[URIRef] = VM.Report
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

    class_class_uri: ClassVar[URIRef] = SH.ValidationReport
    class_class_curie: ClassVar[str] = "sh:ValidationReport"
    class_name: ClassVar[str] = "ValidationReport"
    class_model_uri: ClassVar[URIRef] = VM.ValidationReport

    results: Optional[
        Union[Union[dict, "ValidationResult"], List[Union[dict, "ValidationResult"]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [
            v if isinstance(v, ValidationResult) else ValidationResult(**as_dict(v))
            for v in self.results
        ]

        super().__post_init__(**kwargs)


@dataclass
class RepairReport(Report):
    """
    A report that consists of repair operation results
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM.RepairReport
    class_class_curie: ClassVar[str] = "vm:RepairReport"
    class_name: ClassVar[str] = "RepairReport"
    class_model_uri: ClassVar[URIRef] = VM.RepairReport

    results: Optional[
        Union[Union[dict, "RepairOperation"], List[Union[dict, "RepairOperation"]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.results, list):
            self.results = [self.results] if self.results is not None else []
        self.results = [
            v if isinstance(v, RepairOperation) else RepairOperation(**as_dict(v))
            for v in self.results
        ]

        super().__post_init__(**kwargs)


class Result(YAMLRoot):
    """
    Abstract base class for any individual report result
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM.Result
    class_class_curie: ClassVar[str] = "vm:Result"
    class_name: ClassVar[str] = "Result"
    class_model_uri: ClassVar[URIRef] = VM.Result


@dataclass
class ValidationResult(Result):
    """
    An individual result arising from validation of a data instance using a particular rule
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH.ValidationResult
    class_class_curie: ClassVar[str] = "sh:ValidationResult"
    class_name: ClassVar[str] = "ValidationResult"
    class_model_uri: ClassVar[URIRef] = VM.ValidationResult

    type: Union[str, URIorCURIE] = None
    subject: Union[str, URIorCURIE] = None
    severity: Optional[Union[str, "SeverityOptions"]] = None
    instantiates: Optional[Union[str, URIorCURIE]] = None
    predicate: Optional[Union[str, URIorCURIE]] = None
    object: Optional[Union[str, URIorCURIE]] = None
    object_str: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    info: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, URIorCURIE):
            self.type = URIorCURIE(self.type)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, URIorCURIE):
            self.subject = URIorCURIE(self.subject)

        if self.severity is not None and not isinstance(self.severity, SeverityOptions):
            self.severity = SeverityOptions(self.severity)

        if self.instantiates is not None and not isinstance(self.instantiates, URIorCURIE):
            self.instantiates = URIorCURIE(self.instantiates)

        if self.predicate is not None and not isinstance(self.predicate, URIorCURIE):
            self.predicate = URIorCURIE(self.predicate)

        if self.object is not None and not isinstance(self.object, URIorCURIE):
            self.object = URIorCURIE(self.object)

        if self.object_str is not None and not isinstance(self.object_str, str):
            self.object_str = str(self.object_str)

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if self.info is not None and not isinstance(self.info, str):
            self.info = str(self.info)

        super().__post_init__(**kwargs)


@dataclass
class RepairOperation(Result):
    """
    The result of performing an individual repair
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VM.RepairOperation
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

    class_class_uri: ClassVar[URIRef] = VM.ExternalReferenceValidationResult
    class_class_curie: ClassVar[str] = "vm:ExternalReferenceValidationResult"
    class_name: ClassVar[str] = "ExternalReferenceValidationResult"
    class_model_uri: ClassVar[URIRef] = VM.ExternalReferenceValidationResult

    type: Union[str, URIorCURIE] = None
    subject: Union[str, URIorCURIE] = None
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
    ERROR = PermissibleValue(text="ERROR", meaning=SH.Violation)
    WARNING = PermissibleValue(text="WARNING", meaning=SH.Warning)
    INFO = PermissibleValue(text="INFO", meaning=SH.Info)

    _defn = EnumDefinition(
        name="SeverityOptions",
    )


class ValidationResultType(EnumDefinitionImpl):

    DatatypeConstraintComponent = PermissibleValue(
        text="DatatypeConstraintComponent",
        description="constraint in which the range is a type, and the slot value must conform to the type",
        meaning=SH.DatatypeConstraintComponent,
    )
    MinCountConstraintComponent = PermissibleValue(
        text="MinCountConstraintComponent",
        description="cardinality constraint where the slot value must be greater or equal to a specified minimum",
        meaning=SH.MinCountConstraintComponent,
    )
    MaxCountConstraintComponent = PermissibleValue(
        text="MaxCountConstraintComponent",
        description="cardinality constraint where the slot value must be less than or equal to a specified maximum",
        meaning=SH.MaxCountConstraintComponent,
    )
    DeprecatedPropertyComponent = PermissibleValue(
        text="DeprecatedPropertyComponent",
        description="constraint where the instance slot should not be deprecated",
        meaning=VM.DeprecatedPropertyComponent,
    )
    MaxLengthConstraintComponent = PermissibleValue(
        text="MaxLengthConstraintComponent",
        description="constraint where the slot value must have a length equal to or less than a specified maximum",
        meaning=SH.MaxLengthConstraintComponent,
    )
    MinLengthConstraintComponent = PermissibleValue(
        text="MinLengthConstraintComponent",
        description="constraint where the slot value must have a length equal to or less than a specified maximum",
        meaning=SH.MinLengthConstraintComponent,
    )
    PatternConstraintComponent = PermissibleValue(
        text="PatternConstraintComponent",
        description="constraint where the slot value must match a given regular expression pattern",
        meaning=SH.PatternConstraintComponent,
    )
    ClosedConstraintComponent = PermissibleValue(
        text="ClosedConstraintComponent",
        description="constraint where the slot value must be allowable for the type of an instance",
        meaning=SH.ClosedConstraintComponent,
    )

    _defn = EnumDefinition(
        name="ValidationResultType",
    )


# Slots
class slots:
    pass


slots.type = Slot(
    uri=SH.sourceConstraintComponent,
    name="type",
    curie=SH.curie("sourceConstraintComponent"),
    model_uri=VM.type,
    domain=None,
    range=Union[str, URIorCURIE],
)

slots.subject = Slot(
    uri=SH.focusNode,
    name="subject",
    curie=SH.curie("focusNode"),
    model_uri=VM.subject,
    domain=None,
    range=Union[str, URIorCURIE],
)

slots.instantiates = Slot(
    uri=VM.instantiates,
    name="instantiates",
    curie=VM.curie("instantiates"),
    model_uri=VM.instantiates,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.predicate = Slot(
    uri=VM.predicate,
    name="predicate",
    curie=VM.curie("predicate"),
    model_uri=VM.predicate,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.object = Slot(
    uri=SH.value,
    name="object",
    curie=SH.curie("value"),
    model_uri=VM.object,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.object_str = Slot(
    uri=VM.object_str,
    name="object_str",
    curie=VM.curie("object_str"),
    model_uri=VM.object_str,
    domain=None,
    range=Optional[str],
)

slots.source = Slot(
    uri=VM.source,
    name="source",
    curie=VM.curie("source"),
    model_uri=VM.source,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.severity = Slot(
    uri=SH.resultSeverity,
    name="severity",
    curie=SH.curie("resultSeverity"),
    model_uri=VM.severity,
    domain=None,
    range=Optional[Union[str, "SeverityOptions"]],
)

slots.info = Slot(
    uri=SH.resultMessage,
    name="info",
    curie=SH.curie("resultMessage"),
    model_uri=VM.info,
    domain=None,
    range=Optional[str],
)

slots.results = Slot(
    uri=SH.result,
    name="results",
    curie=SH.curie("result"),
    model_uri=VM.results,
    domain=None,
    range=Optional[Union[Union[dict, Result], List[Union[dict, Result]]]],
)

slots.validationConfiguration__max_number_results_per_type = Slot(
    uri=VM.max_number_results_per_type,
    name="validationConfiguration__max_number_results_per_type",
    curie=VM.curie("max_number_results_per_type"),
    model_uri=VM.validationConfiguration__max_number_results_per_type,
    domain=None,
    range=Optional[int],
)

slots.validationConfiguration__type_severity_map = Slot(
    uri=VM.type_severity_map,
    name="validationConfiguration__type_severity_map",
    curie=VM.curie("type_severity_map"),
    model_uri=VM.validationConfiguration__type_severity_map,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, TypeSeverityKeyValueType], Union[dict, TypeSeverityKeyValue]],
            List[Union[dict, TypeSeverityKeyValue]],
        ]
    ],
)

slots.validationConfiguration__schema_path = Slot(
    uri=VM.schema_path,
    name="validationConfiguration__schema_path",
    curie=VM.curie("schema_path"),
    model_uri=VM.validationConfiguration__schema_path,
    domain=None,
    range=Optional[str],
)

slots.repairConfiguration__validation_configuration = Slot(
    uri=VM.validation_configuration,
    name="repairConfiguration__validation_configuration",
    curie=VM.curie("validation_configuration"),
    model_uri=VM.repairConfiguration__validation_configuration,
    domain=None,
    range=Optional[Union[dict, ValidationConfiguration]],
)

slots.repairConfiguration__dry_run = Slot(
    uri=VM.dry_run,
    name="repairConfiguration__dry_run",
    curie=VM.curie("dry_run"),
    model_uri=VM.repairConfiguration__dry_run,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.typeSeverityKeyValue__type = Slot(
    uri=VM.type,
    name="typeSeverityKeyValue__type",
    curie=VM.curie("type"),
    model_uri=VM.typeSeverityKeyValue__type,
    domain=None,
    range=URIRef,
)

slots.typeSeverityKeyValue__severity = Slot(
    uri=VM.severity,
    name="typeSeverityKeyValue__severity",
    curie=VM.curie("severity"),
    model_uri=VM.typeSeverityKeyValue__severity,
    domain=None,
    range=Optional[Union[str, "SeverityOptions"]],
)

slots.repairOperation__repairs = Slot(
    uri=VM.repairs,
    name="repairOperation__repairs",
    curie=VM.curie("repairs"),
    model_uri=VM.repairOperation__repairs,
    domain=None,
    range=Optional[Union[dict, ValidationResult]],
)

slots.repairOperation__modified = Slot(
    uri=VM.modified,
    name="repairOperation__modified",
    curie=VM.curie("modified"),
    model_uri=VM.repairOperation__modified,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.repairOperation__successful = Slot(
    uri=VM.successful,
    name="repairOperation__successful",
    curie=VM.curie("successful"),
    model_uri=VM.repairOperation__successful,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.repairOperation__info = Slot(
    uri=VM.info,
    name="repairOperation__info",
    curie=VM.curie("info"),
    model_uri=VM.repairOperation__info,
    domain=None,
    range=Optional[str],
)

slots.externalReferenceValidationResult__url = Slot(
    uri=VM.url,
    name="externalReferenceValidationResult__url",
    curie=VM.curie("url"),
    model_uri=VM.externalReferenceValidationResult__url,
    domain=None,
    range=Optional[str],
)

slots.externalReferenceValidationResult__time_checked = Slot(
    uri=VM.time_checked,
    name="externalReferenceValidationResult__time_checked",
    curie=VM.curie("time_checked"),
    model_uri=VM.externalReferenceValidationResult__time_checked,
    domain=None,
    range=Optional[str],
)

slots.externalReferenceValidationResult__number_of_attempts = Slot(
    uri=VM.number_of_attempts,
    name="externalReferenceValidationResult__number_of_attempts",
    curie=VM.curie("number_of_attempts"),
    model_uri=VM.externalReferenceValidationResult__number_of_attempts,
    domain=None,
    range=Optional[int],
)

slots.externalReferenceValidationResult__http_response_code = Slot(
    uri=VM.http_response_code,
    name="externalReferenceValidationResult__http_response_code",
    curie=VM.curie("http_response_code"),
    model_uri=VM.externalReferenceValidationResult__http_response_code,
    domain=None,
    range=Optional[int],
)

slots.ValidationReport_results = Slot(
    uri=SH.result,
    name="ValidationReport_results",
    curie=SH.curie("result"),
    model_uri=VM.ValidationReport_results,
    domain=ValidationReport,
    range=Optional[Union[Union[dict, "ValidationResult"], List[Union[dict, "ValidationResult"]]]],
)

slots.RepairReport_results = Slot(
    uri=SH.result,
    name="RepairReport_results",
    curie=SH.curie("result"),
    model_uri=VM.RepairReport_results,
    domain=RepairReport,
    range=Optional[Union[Union[dict, "RepairOperation"], List[Union[dict, "RepairOperation"]]]],
)
