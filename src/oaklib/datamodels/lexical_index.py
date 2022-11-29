# Auto generated from lexical_index.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-09-21T22:56:24
# Schema: lexical-index
#
# id: https://w3id.org/linkml/lexical_index
# description: A datamodel for representing a lexical index of an ontology. A lexical index is keyed by optionally
#              normalized terms.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions,
)
from linkml_runtime.linkml_model.types import Boolean, String, Uriorcurie
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import (
    Bool,
    URIorCURIE,
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
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LI = CurieNamespace("li", "https://w3id.org/linkml/lexical_index/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = LI


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

    class_class_uri: ClassVar[URIRef] = LI.LexicalIndex
    class_class_curie: ClassVar[str] = "li:LexicalIndex"
    class_name: ClassVar[str] = "LexicalIndex"
    class_model_uri: ClassVar[URIRef] = LI.LexicalIndex

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
    class_model_uri: ClassVar[URIRef] = LI.LexicalGrouping

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
    class_model_uri: ClassVar[URIRef] = LI.RelationshipToTerm

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
        self.pipeline = [
            v
            if isinstance(v, LexicalTransformationPipelineName)
            else LexicalTransformationPipelineName(v)
            for v in self.pipeline
        ]

        if self.synonymized is not None and not isinstance(self.synonymized, Bool):
            self.synonymized = Bool(self.synonymized)

        super().__post_init__(**kwargs)


class Activity(YAMLRoot):
    """
    Generic grouping for any lexical operation
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV.Activity
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = LI.Activity


@dataclass
class LexicalTransformationPipeline(Activity):
    """
    A collection of atomic lexical transformations that are applied in serial fashion
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LI.LexicalTransformationPipeline
    class_class_curie: ClassVar[str] = "li:LexicalTransformationPipeline"
    class_name: ClassVar[str] = "LexicalTransformationPipeline"
    class_model_uri: ClassVar[URIRef] = LI.LexicalTransformationPipeline

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
    class_model_uri: ClassVar[URIRef] = LI.LexicalTransformation

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
    Synonymization = PermissibleValue(
        text="Synonymization", description="Applying synonymizer rules from matcher_rules.yaml"
    )

    _defn = EnumDefinition(
        name="TransformationType",
        description="A controlled datamodels of the types of transformation that can be applied to",
    )


# Slots
class slots:
    pass


slots.lexicalIndex__groupings = Slot(
    uri=LI.groupings,
    name="lexicalIndex__groupings",
    curie=LI.curie("groupings"),
    model_uri=LI.lexicalIndex__groupings,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, LexicalGroupingTerm], Union[dict, LexicalGrouping]],
            List[Union[dict, LexicalGrouping]],
        ]
    ],
)

slots.lexicalIndex__pipelines = Slot(
    uri=LI.pipelines,
    name="lexicalIndex__pipelines",
    curie=LI.curie("pipelines"),
    model_uri=LI.lexicalIndex__pipelines,
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
    uri=LI.term,
    name="lexicalGrouping__term",
    curie=LI.curie("term"),
    model_uri=LI.lexicalGrouping__term,
    domain=None,
    range=URIRef,
)

slots.lexicalGrouping__relationships = Slot(
    uri=LI.relationships,
    name="lexicalGrouping__relationships",
    curie=LI.curie("relationships"),
    model_uri=LI.lexicalGrouping__relationships,
    domain=None,
    range=Optional[Union[Union[dict, RelationshipToTerm], List[Union[dict, RelationshipToTerm]]]],
)

slots.relationshipToTerm__predicate = Slot(
    uri=LI.predicate,
    name="relationshipToTerm__predicate",
    curie=LI.curie("predicate"),
    model_uri=LI.relationshipToTerm__predicate,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.relationshipToTerm__element = Slot(
    uri=LI.element,
    name="relationshipToTerm__element",
    curie=LI.curie("element"),
    model_uri=LI.relationshipToTerm__element,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.relationshipToTerm__element_term = Slot(
    uri=LI.element_term,
    name="relationshipToTerm__element_term",
    curie=LI.curie("element_term"),
    model_uri=LI.relationshipToTerm__element_term,
    domain=None,
    range=Optional[str],
)

slots.relationshipToTerm__source = Slot(
    uri=LI.source,
    name="relationshipToTerm__source",
    curie=LI.curie("source"),
    model_uri=LI.relationshipToTerm__source,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.relationshipToTerm__pipeline = Slot(
    uri=LI.pipeline,
    name="relationshipToTerm__pipeline",
    curie=LI.curie("pipeline"),
    model_uri=LI.relationshipToTerm__pipeline,
    domain=None,
    range=Optional[
        Union[
            Union[str, LexicalTransformationPipelineName],
            List[Union[str, LexicalTransformationPipelineName]],
        ]
    ],
)

slots.relationshipToTerm__synonymized = Slot(
    uri=LI.synonymized,
    name="relationshipToTerm__synonymized",
    curie=LI.curie("synonymized"),
    model_uri=LI.relationshipToTerm__synonymized,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.lexicalTransformationPipeline__name = Slot(
    uri=LI.name,
    name="lexicalTransformationPipeline__name",
    curie=LI.curie("name"),
    model_uri=LI.lexicalTransformationPipeline__name,
    domain=None,
    range=URIRef,
)

slots.lexicalTransformationPipeline__transformations = Slot(
    uri=LI.transformations,
    name="lexicalTransformationPipeline__transformations",
    curie=LI.curie("transformations"),
    model_uri=LI.lexicalTransformationPipeline__transformations,
    domain=None,
    range=Optional[
        Union[Union[dict, LexicalTransformation], List[Union[dict, LexicalTransformation]]]
    ],
)

slots.lexicalTransformation__type = Slot(
    uri=LI.type,
    name="lexicalTransformation__type",
    curie=LI.curie("type"),
    model_uri=LI.lexicalTransformation__type,
    domain=None,
    range=Optional[Union[str, "TransformationType"]],
)

slots.lexicalTransformation__params = Slot(
    uri=LI.params,
    name="lexicalTransformation__params",
    curie=LI.curie("params"),
    model_uri=LI.lexicalTransformation__params,
    domain=None,
    range=Optional[str],
)
