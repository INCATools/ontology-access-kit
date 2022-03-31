# Auto generated from lexical_index.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-03-30T12:03:47
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
from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
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
class LexicalGroupingTerm(extended_str):
    pass


class LexicalTransformationPipelineName(extended_str):
    pass


@dataclass
class LexicalIndex(YAMLRoot):
    """
    An index over an ontology keyed by lexical unit
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.LexicalIndex
    class_class_curie: ClassVar[str] = "reporting:LexicalIndex"
    class_name: ClassVar[str] = "LexicalIndex"
    class_model_uri: ClassVar[URIRef] = REPORTING.LexicalIndex

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

    class_class_uri: ClassVar[URIRef] = REPORTING.LexicalGrouping
    class_class_curie: ClassVar[str] = "reporting:LexicalGrouping"
    class_name: ClassVar[str] = "LexicalGrouping"
    class_model_uri: ClassVar[URIRef] = REPORTING.LexicalGrouping

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

    class_class_uri: ClassVar[URIRef] = REPORTING.RelationshipToTerm
    class_class_curie: ClassVar[str] = "reporting:RelationshipToTerm"
    class_name: ClassVar[str] = "RelationshipToTerm"
    class_model_uri: ClassVar[URIRef] = REPORTING.RelationshipToTerm

    predicate: Optional[Union[str, URIorCURIE]] = None
    element: Optional[Union[str, URIorCURIE]] = None
    element_term: Optional[str] = None
    source: Optional[Union[str, URIorCURIE]] = None
    pipeline: Optional[Union[Union[str, LexicalTransformationPipelineName], List[Union[str, LexicalTransformationPipelineName]]]] = empty_list()

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

        super().__post_init__(**kwargs)


class Activity(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV.Activity
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = REPORTING.Activity


@dataclass
class LexicalTransformationPipeline(Activity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.LexicalTransformationPipeline
    class_class_curie: ClassVar[str] = "reporting:LexicalTransformationPipeline"
    class_name: ClassVar[str] = "LexicalTransformationPipeline"
    class_model_uri: ClassVar[URIRef] = REPORTING.LexicalTransformationPipeline

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
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = REPORTING.LexicalTransformation
    class_class_curie: ClassVar[str] = "reporting:LexicalTransformation"
    class_name: ClassVar[str] = "LexicalTransformation"
    class_model_uri: ClassVar[URIRef] = REPORTING.LexicalTransformation

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

    Stemming = PermissibleValue(text="Stemming")
    Lemmatization = PermissibleValue(text="Lemmatization")
    WordOrderNormalization = PermissibleValue(text="WordOrderNormalization")
    Depluralization = PermissibleValue(text="Depluralization")
    CaseNormalization = PermissibleValue(text="CaseNormalization")
    WhitespaceNormalization = PermissibleValue(text="WhitespaceNormalization")

    _defn = EnumDefinition(
        name="TransformationType",
    )

# Slots
class slots:
    pass

slots.lexicalIndex__groupings = Slot(uri=REPORTING.groupings, name="lexicalIndex__groupings", curie=REPORTING.curie('groupings'),
                   model_uri=REPORTING.lexicalIndex__groupings, domain=None, range=Optional[Union[Dict[Union[str, LexicalGroupingTerm], Union[dict, LexicalGrouping]], List[Union[dict, LexicalGrouping]]]])

slots.lexicalIndex__pipelines = Slot(uri=REPORTING.pipelines, name="lexicalIndex__pipelines", curie=REPORTING.curie('pipelines'),
                   model_uri=REPORTING.lexicalIndex__pipelines, domain=None, range=Optional[Union[Dict[Union[str, LexicalTransformationPipelineName], Union[dict, LexicalTransformationPipeline]], List[Union[dict, LexicalTransformationPipeline]]]])

slots.lexicalGrouping__term = Slot(uri=REPORTING.term, name="lexicalGrouping__term", curie=REPORTING.curie('term'),
                   model_uri=REPORTING.lexicalGrouping__term, domain=None, range=URIRef)

slots.lexicalGrouping__relationships = Slot(uri=REPORTING.relationships, name="lexicalGrouping__relationships", curie=REPORTING.curie('relationships'),
                   model_uri=REPORTING.lexicalGrouping__relationships, domain=None, range=Optional[Union[Union[dict, RelationshipToTerm], List[Union[dict, RelationshipToTerm]]]])

slots.relationshipToTerm__predicate = Slot(uri=REPORTING.predicate, name="relationshipToTerm__predicate", curie=REPORTING.curie('predicate'),
                   model_uri=REPORTING.relationshipToTerm__predicate, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.relationshipToTerm__element = Slot(uri=REPORTING.element, name="relationshipToTerm__element", curie=REPORTING.curie('element'),
                   model_uri=REPORTING.relationshipToTerm__element, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.relationshipToTerm__element_term = Slot(uri=REPORTING.element_term, name="relationshipToTerm__element_term", curie=REPORTING.curie('element_term'),
                   model_uri=REPORTING.relationshipToTerm__element_term, domain=None, range=Optional[str])

slots.relationshipToTerm__source = Slot(uri=REPORTING.source, name="relationshipToTerm__source", curie=REPORTING.curie('source'),
                   model_uri=REPORTING.relationshipToTerm__source, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.relationshipToTerm__pipeline = Slot(uri=REPORTING.pipeline, name="relationshipToTerm__pipeline", curie=REPORTING.curie('pipeline'),
                   model_uri=REPORTING.relationshipToTerm__pipeline, domain=None, range=Optional[Union[Union[str, LexicalTransformationPipelineName], List[Union[str, LexicalTransformationPipelineName]]]])

slots.lexicalTransformationPipeline__name = Slot(uri=REPORTING.name, name="lexicalTransformationPipeline__name", curie=REPORTING.curie('name'),
                   model_uri=REPORTING.lexicalTransformationPipeline__name, domain=None, range=URIRef)

slots.lexicalTransformationPipeline__transformations = Slot(uri=REPORTING.transformations, name="lexicalTransformationPipeline__transformations", curie=REPORTING.curie('transformations'),
                   model_uri=REPORTING.lexicalTransformationPipeline__transformations, domain=None, range=Optional[Union[Union[dict, LexicalTransformation], List[Union[dict, LexicalTransformation]]]])

slots.lexicalTransformation__type = Slot(uri=REPORTING.type, name="lexicalTransformation__type", curie=REPORTING.curie('type'),
                   model_uri=REPORTING.lexicalTransformation__type, domain=None, range=Optional[Union[str, "TransformationType"]])

slots.lexicalTransformation__params = Slot(uri=REPORTING.params, name="lexicalTransformation__params", curie=REPORTING.curie('params'),
                   model_uri=REPORTING.lexicalTransformation__params, domain=None, range=Optional[str])
