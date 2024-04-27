# Auto generated from mapping_rules_datamodel.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-04-25T10:18:46
# Schema: mapping-rules-datamodel
#
# id: https://w3id.org/oak/mapping-rules-datamodel
# description: A datamodel for specifying lexical mapping rules
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
from linkml_runtime.linkml_model.types import Boolean, Float, String, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
MAPPINGRULES = CurieNamespace('mappingrules', 'https://w3id.org/oak/mapping-rules-datamodel/')
ONTOLEXINDEX = CurieNamespace('ontolexindex', 'https://w3id.org/oak/lexical-index/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
SYNONYMIZER = CurieNamespace('synonymizer', 'https://w3id.org/oak/synonymizer-datamodel/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = MAPPINGRULES


# Types
class RegularExpressionString(String):
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "RegularExpressionString"
    type_model_uri = MAPPINGRULES.RegularExpressionString


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

    class_class_uri: ClassVar[URIRef] = MAPPINGRULES["MappingRuleCollection"]
    class_class_curie: ClassVar[str] = "mappingrules:MappingRuleCollection"
    class_name: ClassVar[str] = "MappingRuleCollection"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.MappingRuleCollection

    rules: Optional[Union[Union[dict, "MappingRule"], List[Union[dict, "MappingRule"]]]] = empty_list()
    minimum_confidence: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.rules, list):
            self.rules = [self.rules] if self.rules is not None else []
        self.rules = [v if isinstance(v, MappingRule) else MappingRule(**as_dict(v)) for v in self.rules]

        if self.minimum_confidence is not None and not isinstance(self.minimum_confidence, float):
            self.minimum_confidence = float(self.minimum_confidence)

        super().__post_init__(**kwargs)


@dataclass
class MappingRule(YAMLRoot):
    """
    An individual mapping rule, if preconditions match the postconditions are applied
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MAPPINGRULES["MappingRule"]
    class_class_curie: ClassVar[str] = "mappingrules:MappingRule"
    class_name: ClassVar[str] = "MappingRule"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.MappingRule

    description: Optional[str] = None
    oneway: Optional[Union[bool, Bool]] = False
    preconditions: Optional[Union[dict, "Precondition"]] = None
    postconditions: Optional[Union[dict, "Postcondition"]] = None
    synonymizer: Optional[Union[dict, "Synonymizer"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.oneway is not None and not isinstance(self.oneway, Bool):
            self.oneway = Bool(self.oneway)

        if self.preconditions is not None and not isinstance(self.preconditions, Precondition):
            self.preconditions = Precondition(**as_dict(self.preconditions))

        if self.postconditions is not None and not isinstance(self.postconditions, Postcondition):
            self.postconditions = Postcondition(**as_dict(self.postconditions))

        if self.synonymizer is not None and not isinstance(self.synonymizer, Synonymizer):
            self.synonymizer = Synonymizer(**as_dict(self.synonymizer))

        super().__post_init__(**kwargs)


@dataclass
class Precondition(YAMLRoot):
    """
    A pattern to be matched against an individual SSSOM mapping
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MAPPINGRULES["Precondition"]
    class_class_curie: ClassVar[str] = "mappingrules:Precondition"
    class_name: ClassVar[str] = "Precondition"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.Precondition

    subject_source_one_of: Optional[Union[str, List[str]]] = empty_list()
    object_source_one_of: Optional[Union[str, List[str]]] = empty_list()
    mapping_source_one_of: Optional[Union[str, List[str]]] = empty_list()
    subject_match_field_one_of: Optional[Union[str, List[str]]] = empty_list()
    object_match_field_one_of: Optional[Union[str, List[str]]] = empty_list()
    transformations_included_in: Optional[Union[str, List[str]]] = empty_list()
    predicate_id_one_of: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.subject_source_one_of, list):
            self.subject_source_one_of = [self.subject_source_one_of] if self.subject_source_one_of is not None else []
        self.subject_source_one_of = [v if isinstance(v, str) else str(v) for v in self.subject_source_one_of]

        if not isinstance(self.object_source_one_of, list):
            self.object_source_one_of = [self.object_source_one_of] if self.object_source_one_of is not None else []
        self.object_source_one_of = [v if isinstance(v, str) else str(v) for v in self.object_source_one_of]

        if not isinstance(self.mapping_source_one_of, list):
            self.mapping_source_one_of = [self.mapping_source_one_of] if self.mapping_source_one_of is not None else []
        self.mapping_source_one_of = [v if isinstance(v, str) else str(v) for v in self.mapping_source_one_of]

        if not isinstance(self.subject_match_field_one_of, list):
            self.subject_match_field_one_of = [self.subject_match_field_one_of] if self.subject_match_field_one_of is not None else []
        self.subject_match_field_one_of = [v if isinstance(v, str) else str(v) for v in self.subject_match_field_one_of]

        if not isinstance(self.object_match_field_one_of, list):
            self.object_match_field_one_of = [self.object_match_field_one_of] if self.object_match_field_one_of is not None else []
        self.object_match_field_one_of = [v if isinstance(v, str) else str(v) for v in self.object_match_field_one_of]

        if not isinstance(self.transformations_included_in, list):
            self.transformations_included_in = [self.transformations_included_in] if self.transformations_included_in is not None else []
        self.transformations_included_in = [v if isinstance(v, str) else str(v) for v in self.transformations_included_in]

        if not isinstance(self.predicate_id_one_of, list):
            self.predicate_id_one_of = [self.predicate_id_one_of] if self.predicate_id_one_of is not None else []
        self.predicate_id_one_of = [v if isinstance(v, str) else str(v) for v in self.predicate_id_one_of]

        super().__post_init__(**kwargs)


@dataclass
class Postcondition(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MAPPINGRULES["Postcondition"]
    class_class_curie: ClassVar[str] = "mappingrules:Postcondition"
    class_name: ClassVar[str] = "Postcondition"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.Postcondition

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

    class_class_uri: ClassVar[URIRef] = ONTOLEXINDEX["LexicalIndex"]
    class_class_curie: ClassVar[str] = "ontolexindex:LexicalIndex"
    class_name: ClassVar[str] = "LexicalIndex"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.LexicalIndex

    groupings: Optional[Union[Dict[Union[str, LexicalGroupingTerm], Union[dict, "LexicalGrouping"]], List[Union[dict, "LexicalGrouping"]]]] = empty_dict()
    pipelines: Optional[Union[Dict[Union[str, LexicalTransformationPipelineName], Union[dict, "LexicalTransformationPipeline"]], List[Union[dict, "LexicalTransformationPipeline"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="groupings", slot_type=LexicalGrouping, key_name="term", keyed=True)

        self._normalize_inlined_as_dict(slot_name="pipelines", slot_type=LexicalTransformationPipeline, key_name="name", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class LexicalGrouping(YAMLRoot):
    """
    A grouping of ontology elements by a shared lexical term
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOLEXINDEX["LexicalGrouping"]
    class_class_curie: ClassVar[str] = "ontolexindex:LexicalGrouping"
    class_name: ClassVar[str] = "LexicalGrouping"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.LexicalGrouping

    term: Union[str, LexicalGroupingTerm] = None
    relationships: Optional[Union[Union[dict, "RelationshipToTerm"], List[Union[dict, "RelationshipToTerm"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.term):
            self.MissingRequiredField("term")
        if not isinstance(self.term, LexicalGroupingTerm):
            self.term = LexicalGroupingTerm(self.term)

        if not isinstance(self.relationships, list):
            self.relationships = [self.relationships] if self.relationships is not None else []
        self.relationships = [v if isinstance(v, RelationshipToTerm) else RelationshipToTerm(**as_dict(v)) for v in self.relationships]

        super().__post_init__(**kwargs)


@dataclass
class RelationshipToTerm(YAMLRoot):
    """
    A relationship of an ontology element to a lexical term
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOLEXINDEX["RelationshipToTerm"]
    class_class_curie: ClassVar[str] = "ontolexindex:RelationshipToTerm"
    class_name: ClassVar[str] = "RelationshipToTerm"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.RelationshipToTerm

    predicate: Optional[Union[str, URIorCURIE]] = None
    element: Optional[Union[str, URIorCURIE]] = None
    element_term: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    pipeline: Optional[Union[Union[str, LexicalTransformationPipelineName], List[Union[str, LexicalTransformationPipelineName]]]] = empty_list()
    synonymized: Optional[Union[bool, Bool]] = None

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
        self.pipeline = [v if isinstance(v, LexicalTransformationPipelineName) else LexicalTransformationPipelineName(v) for v in self.pipeline]

        if self.synonymized is not None and not isinstance(self.synonymized, Bool):
            self.synonymized = Bool(self.synonymized)

        super().__post_init__(**kwargs)


class Activity(YAMLRoot):
    """
    Generic grouping for any lexical operation
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.Activity


@dataclass
class LexicalTransformationPipeline(Activity):
    """
    A collection of atomic lexical transformations that are applied in serial fashion
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOLEXINDEX["LexicalTransformationPipeline"]
    class_class_curie: ClassVar[str] = "ontolexindex:LexicalTransformationPipeline"
    class_name: ClassVar[str] = "LexicalTransformationPipeline"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.LexicalTransformationPipeline

    name: Union[str, LexicalTransformationPipelineName] = None
    transformations: Optional[Union[Union[dict, "LexicalTransformation"], List[Union[dict, "LexicalTransformation"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, LexicalTransformationPipelineName):
            self.name = LexicalTransformationPipelineName(self.name)

        if not isinstance(self.transformations, list):
            self.transformations = [self.transformations] if self.transformations is not None else []
        self.transformations = [v if isinstance(v, LexicalTransformation) else LexicalTransformation(**as_dict(v)) for v in self.transformations]

        super().__post_init__(**kwargs)


@dataclass
class LexicalTransformation(Activity):
    """
    An atomic lexical transformation applied on a term (string) yielding a transformed string
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ONTOLEXINDEX["LexicalTransformation"]
    class_class_curie: ClassVar[str] = "ontolexindex:LexicalTransformation"
    class_name: ClassVar[str] = "LexicalTransformation"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.LexicalTransformation

    type: Optional[Union[str, "TransformationType"]] = None
    params: Optional[Union[Union[dict, "Any"], List[Union[dict, "Any"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, TransformationType):
            self.type = TransformationType(self.type)

        super().__post_init__(**kwargs)


Any = Any

@dataclass
class RuleSet(YAMLRoot):
    """
    A set of rules for generating synonyms or alternate lexical elements.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SYNONYMIZER["RuleSet"]
    class_class_curie: ClassVar[str] = "synonymizer:RuleSet"
    class_name: ClassVar[str] = "RuleSet"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.RuleSet

    rules: Optional[Union[Union[dict, "Synonymizer"], List[Union[dict, "Synonymizer"]]]] = empty_list()
    prefix: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.rules, list):
            self.rules = [self.rules] if self.rules is not None else []
        self.rules = [v if isinstance(v, Synonymizer) else Synonymizer(**as_dict(v)) for v in self.rules]

        if self.prefix is not None and not isinstance(self.prefix, str):
            self.prefix = str(self.prefix)

        super().__post_init__(**kwargs)


@dataclass
class Synonymizer(YAMLRoot):
    """
    Specification of a rule for generating a synonym or alternate lexical element.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SYNONYMIZER["Synonymizer"]
    class_class_curie: ClassVar[str] = "synonymizer:Synonymizer"
    class_name: ClassVar[str] = "Synonymizer"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.Synonymizer

    description: Optional[str] = None
    match: Optional[Union[str, RegularExpressionString]] = None
    match_scope: Optional[str] = None
    replacement: Optional[Union[str, RegularExpressionString]] = None
    qualifier: Optional[str] = None
    prefix: Optional[str] = None
    in_place: Optional[Union[bool, Bool]] = None
    tests: Optional[Union[Union[dict, "Test"], List[Union[dict, "Test"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.match is not None and not isinstance(self.match, RegularExpressionString):
            self.match = RegularExpressionString(self.match)

        if self.match_scope is not None and not isinstance(self.match_scope, str):
            self.match_scope = str(self.match_scope)

        if self.replacement is not None and not isinstance(self.replacement, RegularExpressionString):
            self.replacement = RegularExpressionString(self.replacement)

        if self.qualifier is not None and not isinstance(self.qualifier, str):
            self.qualifier = str(self.qualifier)

        if self.prefix is not None and not isinstance(self.prefix, str):
            self.prefix = str(self.prefix)

        if self.in_place is not None and not isinstance(self.in_place, Bool):
            self.in_place = Bool(self.in_place)

        if not isinstance(self.tests, list):
            self.tests = [self.tests] if self.tests is not None else []
        self.tests = [v if isinstance(v, Test) else Test(**as_dict(v)) for v in self.tests]

        super().__post_init__(**kwargs)


@dataclass
class Test(YAMLRoot):
    """
    A unit test for a rule, specifies an intended output for an input
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SYNONYMIZER["Test"]
    class_class_curie: ClassVar[str] = "synonymizer:Test"
    class_name: ClassVar[str] = "Test"
    class_model_uri: ClassVar[URIRef] = MAPPINGRULES.Test

    input: Optional[str] = None
    output: Optional[str] = None
    prefix: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.input is not None and not isinstance(self.input, str):
            self.input = str(self.input)

        if self.output is not None and not isinstance(self.output, str):
            self.output = str(self.output)

        if self.prefix is not None and not isinstance(self.prefix, str):
            self.prefix = str(self.prefix)

        super().__post_init__(**kwargs)


# Enumerations
class TransformationType(EnumDefinitionImpl):
    """
    A controlled datamodels of the types of transformation that can be applied to
    """
    Stemming = PermissibleValue(
        text="Stemming",
        description="Removal of the last few characters of a word to yield a stem term for each word in the term")
    Lemmatization = PermissibleValue(
        text="Lemmatization",
        description="Contextual reduction of a word to its base form for each word in the term")
    WordOrderNormalization = PermissibleValue(
        text="WordOrderNormalization",
        description="reorder words in the term to a standard order such that comparisons are order-independent")
    Depluralization = PermissibleValue(
        text="Depluralization",
        description="Transform plural form to singular form for each word in a term")
    CaseNormalization = PermissibleValue(
        text="CaseNormalization",
        description="Transform term to a standard case, typically lowercase")
    WhitespaceNormalization = PermissibleValue(
        text="WhitespaceNormalization",
        description="Trim whitespace, condense whitespace runs, and transform all non-space whitespace to spaces")
    TermExpanson = PermissibleValue(
        text="TermExpanson",
        description="Expand terms using a dictionary")
    Synonymization = PermissibleValue(
        text="Synonymization",
        description="Applying synonymizer rules from matcher_rules.yaml")

    _defn = EnumDefinition(
        name="TransformationType",
        description="A controlled datamodels of the types of transformation that can be applied to",
    )

# Slots
class slots:
    pass

slots.mappingRuleCollection__rules = Slot(uri=MAPPINGRULES.rules, name="mappingRuleCollection__rules", curie=MAPPINGRULES.curie('rules'),
                   model_uri=MAPPINGRULES.mappingRuleCollection__rules, domain=None, range=Optional[Union[Union[dict, MappingRule], List[Union[dict, MappingRule]]]])

slots.mappingRuleCollection__minimum_confidence = Slot(uri=MAPPINGRULES.minimum_confidence, name="mappingRuleCollection__minimum_confidence", curie=MAPPINGRULES.curie('minimum_confidence'),
                   model_uri=MAPPINGRULES.mappingRuleCollection__minimum_confidence, domain=None, range=Optional[float])

slots.mappingRule__description = Slot(uri=MAPPINGRULES.description, name="mappingRule__description", curie=MAPPINGRULES.curie('description'),
                   model_uri=MAPPINGRULES.mappingRule__description, domain=None, range=Optional[str])

slots.mappingRule__oneway = Slot(uri=MAPPINGRULES.oneway, name="mappingRule__oneway", curie=MAPPINGRULES.curie('oneway'),
                   model_uri=MAPPINGRULES.mappingRule__oneway, domain=None, range=Optional[Union[bool, Bool]])

slots.mappingRule__preconditions = Slot(uri=SH.condition, name="mappingRule__preconditions", curie=SH.curie('condition'),
                   model_uri=MAPPINGRULES.mappingRule__preconditions, domain=None, range=Optional[Union[dict, Precondition]])

slots.mappingRule__postconditions = Slot(uri=MAPPINGRULES.postconditions, name="mappingRule__postconditions", curie=MAPPINGRULES.curie('postconditions'),
                   model_uri=MAPPINGRULES.mappingRule__postconditions, domain=None, range=Optional[Union[dict, Postcondition]])

slots.mappingRule__synonymizer = Slot(uri=MAPPINGRULES.synonymizer, name="mappingRule__synonymizer", curie=MAPPINGRULES.curie('synonymizer'),
                   model_uri=MAPPINGRULES.mappingRule__synonymizer, domain=None, range=Optional[Union[dict, Synonymizer]])

slots.precondition__subject_source_one_of = Slot(uri=MAPPINGRULES.subject_source_one_of, name="precondition__subject_source_one_of", curie=MAPPINGRULES.curie('subject_source_one_of'),
                   model_uri=MAPPINGRULES.precondition__subject_source_one_of, domain=None, range=Optional[Union[str, List[str]]])

slots.precondition__object_source_one_of = Slot(uri=MAPPINGRULES.object_source_one_of, name="precondition__object_source_one_of", curie=MAPPINGRULES.curie('object_source_one_of'),
                   model_uri=MAPPINGRULES.precondition__object_source_one_of, domain=None, range=Optional[Union[str, List[str]]])

slots.precondition__mapping_source_one_of = Slot(uri=MAPPINGRULES.mapping_source_one_of, name="precondition__mapping_source_one_of", curie=MAPPINGRULES.curie('mapping_source_one_of'),
                   model_uri=MAPPINGRULES.precondition__mapping_source_one_of, domain=None, range=Optional[Union[str, List[str]]])

slots.precondition__subject_match_field_one_of = Slot(uri=MAPPINGRULES.subject_match_field_one_of, name="precondition__subject_match_field_one_of", curie=MAPPINGRULES.curie('subject_match_field_one_of'),
                   model_uri=MAPPINGRULES.precondition__subject_match_field_one_of, domain=None, range=Optional[Union[str, List[str]]])

slots.precondition__object_match_field_one_of = Slot(uri=MAPPINGRULES.object_match_field_one_of, name="precondition__object_match_field_one_of", curie=MAPPINGRULES.curie('object_match_field_one_of'),
                   model_uri=MAPPINGRULES.precondition__object_match_field_one_of, domain=None, range=Optional[Union[str, List[str]]])

slots.precondition__transformations_included_in = Slot(uri=MAPPINGRULES.transformations_included_in, name="precondition__transformations_included_in", curie=MAPPINGRULES.curie('transformations_included_in'),
                   model_uri=MAPPINGRULES.precondition__transformations_included_in, domain=None, range=Optional[Union[str, List[str]]])

slots.precondition__predicate_id_one_of = Slot(uri=MAPPINGRULES.predicate_id_one_of, name="precondition__predicate_id_one_of", curie=MAPPINGRULES.curie('predicate_id_one_of'),
                   model_uri=MAPPINGRULES.precondition__predicate_id_one_of, domain=None, range=Optional[Union[str, List[str]]])

slots.postcondition__predicate_id = Slot(uri=MAPPINGRULES.predicate_id, name="postcondition__predicate_id", curie=MAPPINGRULES.curie('predicate_id'),
                   model_uri=MAPPINGRULES.postcondition__predicate_id, domain=None, range=Optional[str])

slots.postcondition__weight = Slot(uri=MAPPINGRULES.weight, name="postcondition__weight", curie=MAPPINGRULES.curie('weight'),
                   model_uri=MAPPINGRULES.postcondition__weight, domain=None, range=Optional[float])

slots.lexicalIndex__groupings = Slot(uri=ONTOLEXINDEX.groupings, name="lexicalIndex__groupings", curie=ONTOLEXINDEX.curie('groupings'),
                   model_uri=MAPPINGRULES.lexicalIndex__groupings, domain=None, range=Optional[Union[Dict[Union[str, LexicalGroupingTerm], Union[dict, LexicalGrouping]], List[Union[dict, LexicalGrouping]]]])

slots.lexicalIndex__pipelines = Slot(uri=ONTOLEXINDEX.pipelines, name="lexicalIndex__pipelines", curie=ONTOLEXINDEX.curie('pipelines'),
                   model_uri=MAPPINGRULES.lexicalIndex__pipelines, domain=None, range=Optional[Union[Dict[Union[str, LexicalTransformationPipelineName], Union[dict, LexicalTransformationPipeline]], List[Union[dict, LexicalTransformationPipeline]]]])

slots.lexicalGrouping__term = Slot(uri=ONTOLEXINDEX.term, name="lexicalGrouping__term", curie=ONTOLEXINDEX.curie('term'),
                   model_uri=MAPPINGRULES.lexicalGrouping__term, domain=None, range=URIRef)

slots.lexicalGrouping__relationships = Slot(uri=ONTOLEXINDEX.relationships, name="lexicalGrouping__relationships", curie=ONTOLEXINDEX.curie('relationships'),
                   model_uri=MAPPINGRULES.lexicalGrouping__relationships, domain=None, range=Optional[Union[Union[dict, RelationshipToTerm], List[Union[dict, RelationshipToTerm]]]])

slots.relationshipToTerm__predicate = Slot(uri=ONTOLEXINDEX.predicate, name="relationshipToTerm__predicate", curie=ONTOLEXINDEX.curie('predicate'),
                   model_uri=MAPPINGRULES.relationshipToTerm__predicate, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.relationshipToTerm__element = Slot(uri=ONTOLEXINDEX.element, name="relationshipToTerm__element", curie=ONTOLEXINDEX.curie('element'),
                   model_uri=MAPPINGRULES.relationshipToTerm__element, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.relationshipToTerm__element_term = Slot(uri=ONTOLEXINDEX.element_term, name="relationshipToTerm__element_term", curie=ONTOLEXINDEX.curie('element_term'),
                   model_uri=MAPPINGRULES.relationshipToTerm__element_term, domain=None, range=Optional[str])

slots.relationshipToTerm__source = Slot(uri=ONTOLEXINDEX.source, name="relationshipToTerm__source", curie=ONTOLEXINDEX.curie('source'),
                   model_uri=MAPPINGRULES.relationshipToTerm__source, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.relationshipToTerm__pipeline = Slot(uri=ONTOLEXINDEX.pipeline, name="relationshipToTerm__pipeline", curie=ONTOLEXINDEX.curie('pipeline'),
                   model_uri=MAPPINGRULES.relationshipToTerm__pipeline, domain=None, range=Optional[Union[Union[str, LexicalTransformationPipelineName], List[Union[str, LexicalTransformationPipelineName]]]])

slots.relationshipToTerm__synonymized = Slot(uri=ONTOLEXINDEX.synonymized, name="relationshipToTerm__synonymized", curie=ONTOLEXINDEX.curie('synonymized'),
                   model_uri=MAPPINGRULES.relationshipToTerm__synonymized, domain=None, range=Optional[Union[bool, Bool]])

slots.lexicalTransformationPipeline__name = Slot(uri=ONTOLEXINDEX.name, name="lexicalTransformationPipeline__name", curie=ONTOLEXINDEX.curie('name'),
                   model_uri=MAPPINGRULES.lexicalTransformationPipeline__name, domain=None, range=URIRef)

slots.lexicalTransformationPipeline__transformations = Slot(uri=ONTOLEXINDEX.transformations, name="lexicalTransformationPipeline__transformations", curie=ONTOLEXINDEX.curie('transformations'),
                   model_uri=MAPPINGRULES.lexicalTransformationPipeline__transformations, domain=None, range=Optional[Union[Union[dict, LexicalTransformation], List[Union[dict, LexicalTransformation]]]])

slots.lexicalTransformation__type = Slot(uri=ONTOLEXINDEX.type, name="lexicalTransformation__type", curie=ONTOLEXINDEX.curie('type'),
                   model_uri=MAPPINGRULES.lexicalTransformation__type, domain=None, range=Optional[Union[str, "TransformationType"]])

slots.lexicalTransformation__params = Slot(uri=ONTOLEXINDEX.params, name="lexicalTransformation__params", curie=ONTOLEXINDEX.curie('params'),
                   model_uri=MAPPINGRULES.lexicalTransformation__params, domain=None, range=Optional[Union[Union[dict, Any], List[Union[dict, Any]]]])

slots.ruleSet__rules = Slot(uri=SYNONYMIZER.rules, name="ruleSet__rules", curie=SYNONYMIZER.curie('rules'),
                   model_uri=MAPPINGRULES.ruleSet__rules, domain=None, range=Optional[Union[Union[dict, Synonymizer], List[Union[dict, Synonymizer]]]])

slots.ruleSet__prefix = Slot(uri=SYNONYMIZER.prefix, name="ruleSet__prefix", curie=SYNONYMIZER.curie('prefix'),
                   model_uri=MAPPINGRULES.ruleSet__prefix, domain=None, range=Optional[str])

slots.synonymizer__description = Slot(uri=SYNONYMIZER.description, name="synonymizer__description", curie=SYNONYMIZER.curie('description'),
                   model_uri=MAPPINGRULES.synonymizer__description, domain=None, range=Optional[str])

slots.synonymizer__match = Slot(uri=SYNONYMIZER.match, name="synonymizer__match", curie=SYNONYMIZER.curie('match'),
                   model_uri=MAPPINGRULES.synonymizer__match, domain=None, range=Optional[Union[str, RegularExpressionString]])

slots.synonymizer__match_scope = Slot(uri=SYNONYMIZER.match_scope, name="synonymizer__match_scope", curie=SYNONYMIZER.curie('match_scope'),
                   model_uri=MAPPINGRULES.synonymizer__match_scope, domain=None, range=Optional[str])

slots.synonymizer__replacement = Slot(uri=SYNONYMIZER.replacement, name="synonymizer__replacement", curie=SYNONYMIZER.curie('replacement'),
                   model_uri=MAPPINGRULES.synonymizer__replacement, domain=None, range=Optional[Union[str, RegularExpressionString]])

slots.synonymizer__qualifier = Slot(uri=SYNONYMIZER.qualifier, name="synonymizer__qualifier", curie=SYNONYMIZER.curie('qualifier'),
                   model_uri=MAPPINGRULES.synonymizer__qualifier, domain=None, range=Optional[str])

slots.synonymizer__prefix = Slot(uri=SYNONYMIZER.prefix, name="synonymizer__prefix", curie=SYNONYMIZER.curie('prefix'),
                   model_uri=MAPPINGRULES.synonymizer__prefix, domain=None, range=Optional[str])

slots.synonymizer__in_place = Slot(uri=SYNONYMIZER.in_place, name="synonymizer__in_place", curie=SYNONYMIZER.curie('in_place'),
                   model_uri=MAPPINGRULES.synonymizer__in_place, domain=None, range=Optional[Union[bool, Bool]])

slots.synonymizer__tests = Slot(uri=SYNONYMIZER.tests, name="synonymizer__tests", curie=SYNONYMIZER.curie('tests'),
                   model_uri=MAPPINGRULES.synonymizer__tests, domain=None, range=Optional[Union[Union[dict, Test], List[Union[dict, Test]]]])

slots.test__input = Slot(uri=SYNONYMIZER.input, name="test__input", curie=SYNONYMIZER.curie('input'),
                   model_uri=MAPPINGRULES.test__input, domain=None, range=Optional[str])

slots.test__output = Slot(uri=SYNONYMIZER.output, name="test__output", curie=SYNONYMIZER.curie('output'),
                   model_uri=MAPPINGRULES.test__output, domain=None, range=Optional[str])

slots.test__prefix = Slot(uri=SYNONYMIZER.prefix, name="test__prefix", curie=SYNONYMIZER.curie('prefix'),
                   model_uri=MAPPINGRULES.test__prefix, domain=None, range=Optional[str])
