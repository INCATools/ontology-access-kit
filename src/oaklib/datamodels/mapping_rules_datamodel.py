# Auto generated from mapping_rules_datamodel.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-03-31T13:26:26
# Schema: mapping-rules
#
# id: https://w3id.org/linkml/mapping_rules_datamodel
# description: A datamodel for specifying lexical mapping rules. NOTE -- this may move to another package
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
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from rdflib import URIRef

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LI = CurieNamespace("li", "https://w3id.org/linkml/lexical_index/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
MRULES = CurieNamespace("mrules", "https://w3id.org/linkml/mapping_rules_datamodel/")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = MRULES


# Types

# Class references
class LexicalGroupingTerm(extended_str):
    pass


class LexicalTransformationPipelineName(extended_str):
    pass


@dataclass
class MappingRuleCollection(YAMLRoot):
    """
    A collection of mapping rules
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MRULES.MappingRuleCollection
    class_class_curie: ClassVar[str] = "mrules:MappingRuleCollection"
    class_name: ClassVar[str] = "MappingRuleCollection"
    class_model_uri: ClassVar[URIRef] = MRULES.MappingRuleCollection

    rules: Optional[
        Union[Union[dict, "MappingRule"], List[Union[dict, "MappingRule"]]]
    ] = empty_list()
    minimum_confidence: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.rules, list):
            self.rules = [self.rules] if self.rules is not None else []
        self.rules = [
            v if isinstance(v, MappingRule) else MappingRule(**as_dict(v)) for v in self.rules
        ]

        if self.minimum_confidence is not None and not isinstance(self.minimum_confidence, float):
            self.minimum_confidence = float(self.minimum_confidence)

        super().__post_init__(**kwargs)


@dataclass
class MappingRule(YAMLRoot):
    """
    An individual mapping rule, if preconditions match the postconditions are applied
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MRULES.MappingRule
    class_class_curie: ClassVar[str] = "mrules:MappingRule"
    class_name: ClassVar[str] = "MappingRule"
    class_model_uri: ClassVar[URIRef] = MRULES.MappingRule

    description: Optional[str] = None
    oneway: Optional[Union[bool, Bool]] = False
    preconditions: Optional[Union[dict, "Precondition"]] = None
    postconditions: Optional[Union[dict, "Postcondition"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.oneway is not None and not isinstance(self.oneway, Bool):
            self.oneway = Bool(self.oneway)

        if self.preconditions is not None and not isinstance(self.preconditions, Precondition):
            self.preconditions = Precondition(**as_dict(self.preconditions))

        if self.postconditions is not None and not isinstance(self.postconditions, Postcondition):
            self.postconditions = Postcondition(**as_dict(self.postconditions))

        super().__post_init__(**kwargs)


@dataclass
class Precondition(YAMLRoot):
    """
    A pattern to be matched against an individual SSSOM mapping
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MRULES.Precondition
    class_class_curie: ClassVar[str] = "mrules:Precondition"
    class_name: ClassVar[str] = "Precondition"
    class_model_uri: ClassVar[URIRef] = MRULES.Precondition

    subject_source_one_of: Optional[Union[str, List[str]]] = empty_list()
    object_source_one_of: Optional[Union[str, List[str]]] = empty_list()
    mapping_source_one_of: Optional[Union[str, List[str]]] = empty_list()
    subject_match_field_one_of: Optional[Union[str, List[str]]] = empty_list()
    object_match_field_one_of: Optional[Union[str, List[str]]] = empty_list()
    transformations_included_in: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.subject_source_one_of, list):
            self.subject_source_one_of = (
                [self.subject_source_one_of] if self.subject_source_one_of is not None else []
            )
        self.subject_source_one_of = [
            v if isinstance(v, str) else str(v) for v in self.subject_source_one_of
        ]

        if not isinstance(self.object_source_one_of, list):
            self.object_source_one_of = (
                [self.object_source_one_of] if self.object_source_one_of is not None else []
            )
        self.object_source_one_of = [
            v if isinstance(v, str) else str(v) for v in self.object_source_one_of
        ]

        if not isinstance(self.mapping_source_one_of, list):
            self.mapping_source_one_of = (
                [self.mapping_source_one_of] if self.mapping_source_one_of is not None else []
            )
        self.mapping_source_one_of = [
            v if isinstance(v, str) else str(v) for v in self.mapping_source_one_of
        ]

        if not isinstance(self.subject_match_field_one_of, list):
            self.subject_match_field_one_of = (
                [self.subject_match_field_one_of]
                if self.subject_match_field_one_of is not None
                else []
            )
        self.subject_match_field_one_of = [
            v if isinstance(v, str) else str(v) for v in self.subject_match_field_one_of
        ]

        if not isinstance(self.object_match_field_one_of, list):
            self.object_match_field_one_of = (
                [self.object_match_field_one_of]
                if self.object_match_field_one_of is not None
                else []
            )
        self.object_match_field_one_of = [
            v if isinstance(v, str) else str(v) for v in self.object_match_field_one_of
        ]

        if not isinstance(self.transformations_included_in, list):
            self.transformations_included_in = (
                [self.transformations_included_in]
                if self.transformations_included_in is not None
                else []
            )
        self.transformations_included_in = [
            v if isinstance(v, str) else str(v) for v in self.transformations_included_in
        ]

        super().__post_init__(**kwargs)


@dataclass
class Postcondition(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MRULES.Postcondition
    class_class_curie: ClassVar[str] = "mrules:Postcondition"
    class_name: ClassVar[str] = "Postcondition"
    class_model_uri: ClassVar[URIRef] = MRULES.Postcondition

    predicate_id: Optional[str] = None
    weight: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.predicate_id is not None and not isinstance(self.predicate_id, str):
            self.predicate_id = str(self.predicate_id)

        if self.weight is not None and not isinstance(self.weight, float):
            self.weight = float(self.weight)

        super().__post_init__(**kwargs)


@dataclass
class LexicalIndex(YAMLRoot):
    """
    An index over an ontology keyed by lexical unit
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LI.LexicalIndex
    class_class_curie: ClassVar[str] = "li:LexicalIndex"
    class_name: ClassVar[str] = "LexicalIndex"
    class_model_uri: ClassVar[URIRef] = MRULES.LexicalIndex

    groupings: Optional[
        Union[
            Dict[Union[str, LexicalGroupingTerm], Union[dict, "LexicalGrouping"]],
            List[Union[dict, "LexicalGrouping"]],
        ]
    ] = empty_dict()
    pipelines: Optional[
        Union[
            Dict[
                Union[str, LexicalTransformationPipelineName],
                Union[dict, "LexicalTransformationPipeline"],
            ],
            List[Union[dict, "LexicalTransformationPipeline"]],
        ]
    ] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(
            slot_name="groupings", slot_type=LexicalGrouping, key_name="term", keyed=True
        )

        self._normalize_inlined_as_dict(
            slot_name="pipelines",
            slot_type=LexicalTransformationPipeline,
            key_name="name",
            keyed=True,
        )

        super().__post_init__(**kwargs)


@dataclass
class LexicalGrouping(YAMLRoot):
    """
    A grouping of ontology elements by a shared lexical term
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LI.LexicalGrouping
    class_class_curie: ClassVar[str] = "li:LexicalGrouping"
    class_name: ClassVar[str] = "LexicalGrouping"
    class_model_uri: ClassVar[URIRef] = MRULES.LexicalGrouping

    term: Union[str, LexicalGroupingTerm] = None
    relationships: Optional[
        Union[Union[dict, "RelationshipToTerm"], List[Union[dict, "RelationshipToTerm"]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.term):
            self.MissingRequiredField("term")
        if not isinstance(self.term, LexicalGroupingTerm):
            self.term = LexicalGroupingTerm(self.term)

        if not isinstance(self.relationships, list):
            self.relationships = [self.relationships] if self.relationships is not None else []
        self.relationships = [
            v if isinstance(v, RelationshipToTerm) else RelationshipToTerm(**as_dict(v))
            for v in self.relationships
        ]

        super().__post_init__(**kwargs)


@dataclass
class RelationshipToTerm(YAMLRoot):
    """
    A relationship of an ontology element to a lexical term
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LI.RelationshipToTerm
    class_class_curie: ClassVar[str] = "li:RelationshipToTerm"
    class_name: ClassVar[str] = "RelationshipToTerm"
    class_model_uri: ClassVar[URIRef] = MRULES.RelationshipToTerm

    predicate: Optional[Union[str, URIorCURIE]] = None
    element: Optional[Union[str, URIorCURIE]] = None
    element_term: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    pipeline: Optional[
        Union[
            Union[str, LexicalTransformationPipelineName],
            List[Union[str, LexicalTransformationPipelineName]],
        ]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.predicate is not None and not isinstance(self.predicate, URIorCURIE):
            self.predicate = URIorCURIE(self.predicate)

        if self.element is not None and not isinstance(self.element, URIorCURIE):
            self.element = URIorCURIE(self.element)

        if self.element_term is not None and not isinstance(self.element_term, str):
            self.element_term = str(self.element_term)

        if self.source is not None and not isinstance(self.source, URIorCURIE):
            self.source = URIorCURIE(self.source)

        if not isinstance(self.pipeline, list):
            self.pipeline = [self.pipeline] if self.pipeline is not None else []
        self.pipeline = [
            v
            if isinstance(v, LexicalTransformationPipelineName)
            else LexicalTransformationPipelineName(v)
            for v in self.pipeline
        ]

        super().__post_init__(**kwargs)


class Activity(YAMLRoot):
    """
    Generic grouping for any lexical operation
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV.Activity
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = MRULES.Activity


@dataclass
class LexicalTransformationPipeline(Activity):
    """
    A collection of atomic lexical transformations that are applied in serial fashion
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LI.LexicalTransformationPipeline
    class_class_curie: ClassVar[str] = "li:LexicalTransformationPipeline"
    class_name: ClassVar[str] = "LexicalTransformationPipeline"
    class_model_uri: ClassVar[URIRef] = MRULES.LexicalTransformationPipeline

    name: Union[str, LexicalTransformationPipelineName] = None
    transformations: Optional[
        Union[Union[dict, "LexicalTransformation"], List[Union[dict, "LexicalTransformation"]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, LexicalTransformationPipelineName):
            self.name = LexicalTransformationPipelineName(self.name)

        if not isinstance(self.transformations, list):
            self.transformations = (
                [self.transformations] if self.transformations is not None else []
            )
        self.transformations = [
            v if isinstance(v, LexicalTransformation) else LexicalTransformation(**as_dict(v))
            for v in self.transformations
        ]

        super().__post_init__(**kwargs)


@dataclass
class LexicalTransformation(Activity):
    """
    An atomic lexical transformation applied on a term (string) yielding a transformed string
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LI.LexicalTransformation
    class_class_curie: ClassVar[str] = "li:LexicalTransformation"
    class_name: ClassVar[str] = "LexicalTransformation"
    class_model_uri: ClassVar[URIRef] = MRULES.LexicalTransformation

    type: Optional[Union[str, "TransformationType"]] = None
    params: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, TransformationType):
            self.type = TransformationType(self.type)

        if self.params is not None and not isinstance(self.params, str):
            self.params = str(self.params)

        super().__post_init__(**kwargs)


# Enumerations
class TransformationType(EnumDefinitionImpl):
    """
    A controlled datamodels of the types of transformation that can be applied to
    """

    Stemming = PermissibleValue(
        text="Stemming",
        description="Removal of the last few characters of a word to yield a stem term for each word in the term",
    )
    Lemmatization = PermissibleValue(
        text="Lemmatization",
        description="Contextual reduction of a word to its base form for each word in the term",
    )
    WordOrderNormalization = PermissibleValue(
        text="WordOrderNormalization",
        description="reorder words in the term to a standard order such that comparisons are order-independent",
    )
    Depluralization = PermissibleValue(
        text="Depluralization",
        description="Transform plural form to singular form for each word in a term",
    )
    CaseNormalization = PermissibleValue(
        text="CaseNormalization",
        description="Transform term to a standard case, typically lowercase",
    )
    WhitespaceNormalization = PermissibleValue(
        text="WhitespaceNormalization",
        description="Trim whitespace, condense whitespace runs, and transform all non-space whitespace to spaces",
    )
    TermExpanson = PermissibleValue(
        text="TermExpanson", description="Expand terms using a dictionary"
    )

    _defn = EnumDefinition(
        name="TransformationType",
        description="A controlled datamodels of the types of transformation that can be applied to",
    )


# Slots
class slots:
    pass


slots.mappingRuleCollection__rules = Slot(
    uri=MRULES.rules,
    name="mappingRuleCollection__rules",
    curie=MRULES.curie("rules"),
    model_uri=MRULES.mappingRuleCollection__rules,
    domain=None,
    range=Optional[Union[Union[dict, MappingRule], List[Union[dict, MappingRule]]]],
)

slots.mappingRuleCollection__minimum_confidence = Slot(
    uri=MRULES.minimum_confidence,
    name="mappingRuleCollection__minimum_confidence",
    curie=MRULES.curie("minimum_confidence"),
    model_uri=MRULES.mappingRuleCollection__minimum_confidence,
    domain=None,
    range=Optional[float],
)

slots.mappingRule__description = Slot(
    uri=MRULES.description,
    name="mappingRule__description",
    curie=MRULES.curie("description"),
    model_uri=MRULES.mappingRule__description,
    domain=None,
    range=Optional[str],
)

slots.mappingRule__oneway = Slot(
    uri=MRULES.oneway,
    name="mappingRule__oneway",
    curie=MRULES.curie("oneway"),
    model_uri=MRULES.mappingRule__oneway,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.mappingRule__preconditions = Slot(
    uri=SH.condition,
    name="mappingRule__preconditions",
    curie=SH.curie("condition"),
    model_uri=MRULES.mappingRule__preconditions,
    domain=None,
    range=Optional[Union[dict, Precondition]],
)

slots.mappingRule__postconditions = Slot(
    uri=MRULES.postconditions,
    name="mappingRule__postconditions",
    curie=MRULES.curie("postconditions"),
    model_uri=MRULES.mappingRule__postconditions,
    domain=None,
    range=Optional[Union[dict, Postcondition]],
)

slots.precondition__subject_source_one_of = Slot(
    uri=MRULES.subject_source_one_of,
    name="precondition__subject_source_one_of",
    curie=MRULES.curie("subject_source_one_of"),
    model_uri=MRULES.precondition__subject_source_one_of,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.precondition__object_source_one_of = Slot(
    uri=MRULES.object_source_one_of,
    name="precondition__object_source_one_of",
    curie=MRULES.curie("object_source_one_of"),
    model_uri=MRULES.precondition__object_source_one_of,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.precondition__mapping_source_one_of = Slot(
    uri=MRULES.mapping_source_one_of,
    name="precondition__mapping_source_one_of",
    curie=MRULES.curie("mapping_source_one_of"),
    model_uri=MRULES.precondition__mapping_source_one_of,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.precondition__subject_match_field_one_of = Slot(
    uri=MRULES.subject_match_field_one_of,
    name="precondition__subject_match_field_one_of",
    curie=MRULES.curie("subject_match_field_one_of"),
    model_uri=MRULES.precondition__subject_match_field_one_of,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.precondition__object_match_field_one_of = Slot(
    uri=MRULES.object_match_field_one_of,
    name="precondition__object_match_field_one_of",
    curie=MRULES.curie("object_match_field_one_of"),
    model_uri=MRULES.precondition__object_match_field_one_of,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.precondition__transformations_included_in = Slot(
    uri=MRULES.transformations_included_in,
    name="precondition__transformations_included_in",
    curie=MRULES.curie("transformations_included_in"),
    model_uri=MRULES.precondition__transformations_included_in,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.postcondition__predicate_id = Slot(
    uri=MRULES.predicate_id,
    name="postcondition__predicate_id",
    curie=MRULES.curie("predicate_id"),
    model_uri=MRULES.postcondition__predicate_id,
    domain=None,
    range=Optional[str],
)

slots.postcondition__weight = Slot(
    uri=MRULES.weight,
    name="postcondition__weight",
    curie=MRULES.curie("weight"),
    model_uri=MRULES.postcondition__weight,
    domain=None,
    range=Optional[float],
)

slots.lexicalIndex__groupings = Slot(
    uri=MRULES.groupings,
    name="lexicalIndex__groupings",
    curie=MRULES.curie("groupings"),
    model_uri=MRULES.lexicalIndex__groupings,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, LexicalGroupingTerm], Union[dict, LexicalGrouping]],
            List[Union[dict, LexicalGrouping]],
        ]
    ],
)

slots.lexicalIndex__pipelines = Slot(
    uri=MRULES.pipelines,
    name="lexicalIndex__pipelines",
    curie=MRULES.curie("pipelines"),
    model_uri=MRULES.lexicalIndex__pipelines,
    domain=None,
    range=Optional[
        Union[
            Dict[
                Union[str, LexicalTransformationPipelineName],
                Union[dict, LexicalTransformationPipeline],
            ],
            List[Union[dict, LexicalTransformationPipeline]],
        ]
    ],
)

slots.lexicalGrouping__term = Slot(
    uri=MRULES.term,
    name="lexicalGrouping__term",
    curie=MRULES.curie("term"),
    model_uri=MRULES.lexicalGrouping__term,
    domain=None,
    range=URIRef,
)

slots.lexicalGrouping__relationships = Slot(
    uri=MRULES.relationships,
    name="lexicalGrouping__relationships",
    curie=MRULES.curie("relationships"),
    model_uri=MRULES.lexicalGrouping__relationships,
    domain=None,
    range=Optional[Union[Union[dict, RelationshipToTerm], List[Union[dict, RelationshipToTerm]]]],
)

slots.relationshipToTerm__predicate = Slot(
    uri=MRULES.predicate,
    name="relationshipToTerm__predicate",
    curie=MRULES.curie("predicate"),
    model_uri=MRULES.relationshipToTerm__predicate,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.relationshipToTerm__element = Slot(
    uri=MRULES.element,
    name="relationshipToTerm__element",
    curie=MRULES.curie("element"),
    model_uri=MRULES.relationshipToTerm__element,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.relationshipToTerm__element_term = Slot(
    uri=MRULES.element_term,
    name="relationshipToTerm__element_term",
    curie=MRULES.curie("element_term"),
    model_uri=MRULES.relationshipToTerm__element_term,
    domain=None,
    range=Optional[str],
)

slots.relationshipToTerm__source = Slot(
    uri=MRULES.source,
    name="relationshipToTerm__source",
    curie=MRULES.curie("source"),
    model_uri=MRULES.relationshipToTerm__source,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.relationshipToTerm__pipeline = Slot(
    uri=MRULES.pipeline,
    name="relationshipToTerm__pipeline",
    curie=MRULES.curie("pipeline"),
    model_uri=MRULES.relationshipToTerm__pipeline,
    domain=None,
    range=Optional[
        Union[
            Union[str, LexicalTransformationPipelineName],
            List[Union[str, LexicalTransformationPipelineName]],
        ]
    ],
)

slots.lexicalTransformationPipeline__name = Slot(
    uri=MRULES.name,
    name="lexicalTransformationPipeline__name",
    curie=MRULES.curie("name"),
    model_uri=MRULES.lexicalTransformationPipeline__name,
    domain=None,
    range=URIRef,
)

slots.lexicalTransformationPipeline__transformations = Slot(
    uri=MRULES.transformations,
    name="lexicalTransformationPipeline__transformations",
    curie=MRULES.curie("transformations"),
    model_uri=MRULES.lexicalTransformationPipeline__transformations,
    domain=None,
    range=Optional[
        Union[Union[dict, LexicalTransformation], List[Union[dict, LexicalTransformation]]]
    ],
)

slots.lexicalTransformation__type = Slot(
    uri=MRULES.type,
    name="lexicalTransformation__type",
    curie=MRULES.curie("type"),
    model_uri=MRULES.lexicalTransformation__type,
    domain=None,
    range=Optional[Union[str, "TransformationType"]],
)

slots.lexicalTransformation__params = Slot(
    uri=MRULES.params,
    name="lexicalTransformation__params",
    curie=MRULES.curie("params"),
    model_uri=MRULES.lexicalTransformation__params,
    domain=None,
    range=Optional[str],
)
