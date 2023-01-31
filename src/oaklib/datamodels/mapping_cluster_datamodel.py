# Auto generated from mapping_cluster_datamodel.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-01-30T17:20:06
# Schema: mapping-cluster
#
# id: https://w3id.org/linkml/oaklib/cluster
# description: A datamodel for specifying mapping clusters, such as those retrieved from boomer. A mapping cluster
#              is the cluster formed from all potential and actual links between a set of ontology entities, such
#              as terms/classes. - Potential links come from heuristic processes such as lexical alignment, and
#              have probabilities associated - Actual links come from the asserted logical axioms in the ontology,
#              typically subClassOf A *solution* for the cluster is an interpretation of potential links, aka
#              hypothetical axioms. The probability of a solution is Pr(H|A), i.e. the probability of the set of
#              hypothetical axiom interpretations given the set of actual axioms: ``` P(A|H) P(H) Pr(H|A) =
#              ----------- P(A) ``` The term P(H) represents the *prior* probability of the set of hypothetical
#              axioms, multiplying all individual prior probabilities. The term P(A|H) represents the
#              *conditional* probability of the axioms given the hypotheses, i.e the likelihood of the
#              hypothetical axioms given actual axioms. Tools such as boomer treat this as a constant for all
#              satisfiable solutions. If a solution H,A is unsatisfiable, then P(A|H) = 0
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
from linkml_runtime.linkml_model.types import (
    Boolean,
    Datetime,
    Float,
    String,
    Uriorcurie,
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import (
    Bool,
    URIorCURIE,
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
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LI = CurieNamespace("li", "https://w3id.org/linkml/lexical_index/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
MCLUSTER = CurieNamespace("mcluster", "https://w3id.org/linkml/oaklib/cluster")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
SSSOM = CurieNamespace("sssom", "https://w3id.org/sssom/")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = MCLUSTER


# Types
class Probability(Float):
    type_class_uri = XSD.float
    type_class_curie = "xsd:float"
    type_name = "Probability"
    type_model_uri = MCLUSTER.Probability


class NaturalLogProbability(Float):
    type_class_uri = XSD.float
    type_class_curie = "xsd:float"
    type_name = "NaturalLogProbability"
    type_model_uri = MCLUSTER.NaturalLogProbability


class ImageLocation(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "ImageLocation"
    type_model_uri = MCLUSTER.ImageLocation


class DataObjectLocation(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "DataObjectLocation"
    type_model_uri = MCLUSTER.DataObjectLocation


# Class references
class MappingClusterId(extended_str):
    pass


class PredicateProbabilityPredicateId(extended_str):
    pass


class LexicalGroupingTerm(extended_str):
    pass


class LexicalTransformationPipelineName(extended_str):
    pass


@dataclass
class MappingClusterReport(YAMLRoot):
    """
    A collection of equivalence clusters
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MCLUSTER.MappingClusterReport
    class_class_curie: ClassVar[str] = "mcluster:MappingClusterReport"
    class_name: ClassVar[str] = "MappingClusterReport"
    class_model_uri: ClassVar[URIRef] = MCLUSTER.MappingClusterReport

    clusters: Optional[
        Union[
            Dict[Union[str, MappingClusterId], Union[dict, "MappingCluster"]],
            List[Union[dict, "MappingCluster"]],
        ]
    ] = empty_dict()
    started_at_time: Optional[Union[str, XSDDateTime]] = None
    ended_at_time: Optional[Union[str, XSDDateTime]] = None
    input_ontology_path: Optional[str] = None
    input_ptable_path: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(
            slot_name="clusters", slot_type=MappingCluster, key_name="id", keyed=True
        )

        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDateTime):
            self.started_at_time = XSDDateTime(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDateTime):
            self.ended_at_time = XSDDateTime(self.ended_at_time)

        if self.input_ontology_path is not None and not isinstance(self.input_ontology_path, str):
            self.input_ontology_path = str(self.input_ontology_path)

        if self.input_ptable_path is not None and not isinstance(self.input_ptable_path, str):
            self.input_ptable_path = str(self.input_ptable_path)

        super().__post_init__(**kwargs)


@dataclass
class MappingCluster(YAMLRoot):
    """
    An individual mapping rule, if preconditions match the postconditions are applied
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MCLUSTER.MappingCluster
    class_class_curie: ClassVar[str] = "mcluster:MappingCluster"
    class_name: ClassVar[str] = "MappingCluster"
    class_model_uri: ClassVar[URIRef] = MCLUSTER.MappingCluster

    id: Union[str, MappingClusterId] = None
    name: Optional[str] = None
    method: Optional[str] = None
    is_singleton: Optional[Union[bool, Bool]] = None
    boomer_score: Optional[Union[float, NaturalLogProbability]] = None
    subsequent_scores: Optional[
        Union[Union[float, NaturalLogProbability], List[Union[float, NaturalLogProbability]]]
    ] = empty_list()
    log_joint_probability: Optional[Union[float, NaturalLogProbability]] = None
    posterior_probability: Optional[Union[float, Probability]] = None
    confidence: Optional[Union[float, Probability]] = None
    is_resolved: Optional[Union[bool, Bool]] = None
    resolved_mappings: Optional[
        Union[Union[dict, "SimpleMapping"], List[Union[dict, "SimpleMapping"]]]
    ] = empty_list()
    input_mappings: Optional[
        Union[Union[dict, "SimpleMapping"], List[Union[dict, "SimpleMapping"]]]
    ] = empty_list()
    subsequent_raw_scores: Optional[Union[float, List[float]]] = empty_list()
    depiction: Optional[Union[str, ImageLocation]] = None
    data_objects: Optional[Union[str, DataObjectLocation]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MappingClusterId):
            self.id = MappingClusterId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.method is not None and not isinstance(self.method, str):
            self.method = str(self.method)

        if self.is_singleton is not None and not isinstance(self.is_singleton, Bool):
            self.is_singleton = Bool(self.is_singleton)

        if self.boomer_score is not None and not isinstance(
            self.boomer_score, NaturalLogProbability
        ):
            self.boomer_score = NaturalLogProbability(self.boomer_score)

        if not isinstance(self.subsequent_scores, list):
            self.subsequent_scores = (
                [self.subsequent_scores] if self.subsequent_scores is not None else []
            )
        self.subsequent_scores = [
            v if isinstance(v, NaturalLogProbability) else NaturalLogProbability(v)
            for v in self.subsequent_scores
        ]

        if self.log_joint_probability is not None and not isinstance(
            self.log_joint_probability, NaturalLogProbability
        ):
            self.log_joint_probability = NaturalLogProbability(self.log_joint_probability)

        if self.posterior_probability is not None and not isinstance(
            self.posterior_probability, Probability
        ):
            self.posterior_probability = Probability(self.posterior_probability)

        if self.confidence is not None and not isinstance(self.confidence, Probability):
            self.confidence = Probability(self.confidence)

        if self.is_resolved is not None and not isinstance(self.is_resolved, Bool):
            self.is_resolved = Bool(self.is_resolved)

        if not isinstance(self.resolved_mappings, list):
            self.resolved_mappings = (
                [self.resolved_mappings] if self.resolved_mappings is not None else []
            )
        self.resolved_mappings = [
            v if isinstance(v, SimpleMapping) else SimpleMapping(**as_dict(v))
            for v in self.resolved_mappings
        ]

        if not isinstance(self.input_mappings, list):
            self.input_mappings = [self.input_mappings] if self.input_mappings is not None else []
        self.input_mappings = [
            v if isinstance(v, SimpleMapping) else SimpleMapping(**as_dict(v))
            for v in self.input_mappings
        ]

        if not isinstance(self.subsequent_raw_scores, list):
            self.subsequent_raw_scores = (
                [self.subsequent_raw_scores] if self.subsequent_raw_scores is not None else []
            )
        self.subsequent_raw_scores = [
            v if isinstance(v, float) else float(v) for v in self.subsequent_raw_scores
        ]

        if self.depiction is not None and not isinstance(self.depiction, ImageLocation):
            self.depiction = ImageLocation(self.depiction)

        if self.data_objects is not None and not isinstance(self.data_objects, DataObjectLocation):
            self.data_objects = DataObjectLocation(self.data_objects)

        super().__post_init__(**kwargs)


@dataclass
class SimpleMapping(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MCLUSTER.SimpleMapping
    class_class_curie: ClassVar[str] = "mcluster:SimpleMapping"
    class_name: ClassVar[str] = "SimpleMapping"
    class_model_uri: ClassVar[URIRef] = MCLUSTER.SimpleMapping

    cluster_id: Optional[Union[str, MappingClusterId]] = None
    subject_id: Optional[str] = None
    subject_label: Optional[str] = None
    predicate_id: Optional[str] = None
    predicate_label: Optional[str] = None
    object_id: Optional[str] = None
    object_label: Optional[str] = None
    is_most_probable: Optional[Union[bool, Bool]] = None
    prior_probability: Optional[Union[float, Probability]] = None
    posterior_probability: Optional[Union[float, Probability]] = None
    predicate_probabilities: Optional[
        Union[
            Union[str, PredicateProbabilityPredicateId],
            List[Union[str, PredicateProbabilityPredicateId]],
        ]
    ] = empty_list()
    confidence: Optional[Union[float, Probability]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.cluster_id is not None and not isinstance(self.cluster_id, MappingClusterId):
            self.cluster_id = MappingClusterId(self.cluster_id)

        if self.subject_id is not None and not isinstance(self.subject_id, str):
            self.subject_id = str(self.subject_id)

        if self.subject_label is not None and not isinstance(self.subject_label, str):
            self.subject_label = str(self.subject_label)

        if self.predicate_id is not None and not isinstance(self.predicate_id, str):
            self.predicate_id = str(self.predicate_id)

        if self.predicate_label is not None and not isinstance(self.predicate_label, str):
            self.predicate_label = str(self.predicate_label)

        if self.object_id is not None and not isinstance(self.object_id, str):
            self.object_id = str(self.object_id)

        if self.object_label is not None and not isinstance(self.object_label, str):
            self.object_label = str(self.object_label)

        if self.is_most_probable is not None and not isinstance(self.is_most_probable, Bool):
            self.is_most_probable = Bool(self.is_most_probable)

        if self.prior_probability is not None and not isinstance(
            self.prior_probability, Probability
        ):
            self.prior_probability = Probability(self.prior_probability)

        if self.posterior_probability is not None and not isinstance(
            self.posterior_probability, Probability
        ):
            self.posterior_probability = Probability(self.posterior_probability)

        if not isinstance(self.predicate_probabilities, list):
            self.predicate_probabilities = (
                [self.predicate_probabilities] if self.predicate_probabilities is not None else []
            )
        self.predicate_probabilities = [
            v
            if isinstance(v, PredicateProbabilityPredicateId)
            else PredicateProbabilityPredicateId(v)
            for v in self.predicate_probabilities
        ]

        if self.confidence is not None and not isinstance(self.confidence, Probability):
            self.confidence = Probability(self.confidence)

        super().__post_init__(**kwargs)


@dataclass
class PredicateProbability(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MCLUSTER.PredicateProbability
    class_class_curie: ClassVar[str] = "mcluster:PredicateProbability"
    class_name: ClassVar[str] = "PredicateProbability"
    class_model_uri: ClassVar[URIRef] = MCLUSTER.PredicateProbability

    predicate_id: Union[str, PredicateProbabilityPredicateId] = None
    probability: Optional[Union[float, Probability]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.predicate_id):
            self.MissingRequiredField("predicate_id")
        if not isinstance(self.predicate_id, PredicateProbabilityPredicateId):
            self.predicate_id = PredicateProbabilityPredicateId(self.predicate_id)

        if self.probability is not None and not isinstance(self.probability, Probability):
            self.probability = Probability(self.probability)

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
    class_model_uri: ClassVar[URIRef] = MCLUSTER.LexicalIndex

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
    class_model_uri: ClassVar[URIRef] = MCLUSTER.LexicalGrouping

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
    class_model_uri: ClassVar[URIRef] = MCLUSTER.RelationshipToTerm

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
    class_model_uri: ClassVar[URIRef] = MCLUSTER.Activity


@dataclass
class LexicalTransformationPipeline(Activity):
    """
    A collection of atomic lexical transformations that are applied in serial fashion
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LI.LexicalTransformationPipeline
    class_class_curie: ClassVar[str] = "li:LexicalTransformationPipeline"
    class_name: ClassVar[str] = "LexicalTransformationPipeline"
    class_model_uri: ClassVar[URIRef] = MCLUSTER.LexicalTransformationPipeline

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
    class_model_uri: ClassVar[URIRef] = MCLUSTER.LexicalTransformation

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


slots.mappingClusterReport__clusters = Slot(
    uri=MCLUSTER.clusters,
    name="mappingClusterReport__clusters",
    curie=MCLUSTER.curie("clusters"),
    model_uri=MCLUSTER.mappingClusterReport__clusters,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, MappingClusterId], Union[dict, MappingCluster]],
            List[Union[dict, MappingCluster]],
        ]
    ],
)

slots.mappingClusterReport__started_at_time = Slot(
    uri=MCLUSTER.started_at_time,
    name="mappingClusterReport__started_at_time",
    curie=MCLUSTER.curie("started_at_time"),
    model_uri=MCLUSTER.mappingClusterReport__started_at_time,
    domain=None,
    range=Optional[Union[str, XSDDateTime]],
)

slots.mappingClusterReport__ended_at_time = Slot(
    uri=MCLUSTER.ended_at_time,
    name="mappingClusterReport__ended_at_time",
    curie=MCLUSTER.curie("ended_at_time"),
    model_uri=MCLUSTER.mappingClusterReport__ended_at_time,
    domain=None,
    range=Optional[Union[str, XSDDateTime]],
)

slots.mappingClusterReport__input_ontology_path = Slot(
    uri=MCLUSTER.input_ontology_path,
    name="mappingClusterReport__input_ontology_path",
    curie=MCLUSTER.curie("input_ontology_path"),
    model_uri=MCLUSTER.mappingClusterReport__input_ontology_path,
    domain=None,
    range=Optional[str],
)

slots.mappingClusterReport__input_ptable_path = Slot(
    uri=MCLUSTER.input_ptable_path,
    name="mappingClusterReport__input_ptable_path",
    curie=MCLUSTER.curie("input_ptable_path"),
    model_uri=MCLUSTER.mappingClusterReport__input_ptable_path,
    domain=None,
    range=Optional[str],
)

slots.mappingCluster__id = Slot(
    uri=MCLUSTER.id,
    name="mappingCluster__id",
    curie=MCLUSTER.curie("id"),
    model_uri=MCLUSTER.mappingCluster__id,
    domain=None,
    range=URIRef,
)

slots.mappingCluster__name = Slot(
    uri=MCLUSTER.name,
    name="mappingCluster__name",
    curie=MCLUSTER.curie("name"),
    model_uri=MCLUSTER.mappingCluster__name,
    domain=None,
    range=Optional[str],
)

slots.mappingCluster__method = Slot(
    uri=MCLUSTER.method,
    name="mappingCluster__method",
    curie=MCLUSTER.curie("method"),
    model_uri=MCLUSTER.mappingCluster__method,
    domain=None,
    range=Optional[str],
)

slots.mappingCluster__is_singleton = Slot(
    uri=MCLUSTER.is_singleton,
    name="mappingCluster__is_singleton",
    curie=MCLUSTER.curie("is_singleton"),
    model_uri=MCLUSTER.mappingCluster__is_singleton,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.mappingCluster__log_prior_probability = Slot(
    uri=MCLUSTER.boomer_score,
    name="mappingCluster__log_prior_probability",
    curie=MCLUSTER.curie("boomer_score"),
    model_uri=MCLUSTER.mappingCluster__log_prior_probability,
    domain=None,
    range=Optional[Union[float, NaturalLogProbability]],
)

slots.mappingCluster__subsequent_log_prior_probabilities = Slot(
    uri=MCLUSTER.subsequent_scores,
    name="mappingCluster__subsequent_log_prior_probabilities",
    curie=MCLUSTER.curie("subsequent_scores"),
    model_uri=MCLUSTER.mappingCluster__subsequent_log_prior_probabilities,
    domain=None,
    range=Optional[
        Union[Union[float, NaturalLogProbability], List[Union[float, NaturalLogProbability]]]
    ],
)

slots.mappingCluster__log_joint_probability = Slot(
    uri=MCLUSTER.log_joint_probability,
    name="mappingCluster__log_joint_probability",
    curie=MCLUSTER.curie("log_joint_probability"),
    model_uri=MCLUSTER.mappingCluster__log_joint_probability,
    domain=None,
    range=Optional[Union[float, NaturalLogProbability]],
)

slots.mappingCluster__posterior_probability = Slot(
    uri=MCLUSTER.posterior_probability,
    name="mappingCluster__posterior_probability",
    curie=MCLUSTER.curie("posterior_probability"),
    model_uri=MCLUSTER.mappingCluster__posterior_probability,
    domain=None,
    range=Optional[Union[float, Probability]],
)

slots.mappingCluster__confidence = Slot(
    uri=MCLUSTER.confidence,
    name="mappingCluster__confidence",
    curie=MCLUSTER.curie("confidence"),
    model_uri=MCLUSTER.mappingCluster__confidence,
    domain=None,
    range=Optional[Union[float, Probability]],
)

slots.mappingCluster__is_resolved = Slot(
    uri=MCLUSTER.is_resolved,
    name="mappingCluster__is_resolved",
    curie=MCLUSTER.curie("is_resolved"),
    model_uri=MCLUSTER.mappingCluster__is_resolved,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.mappingCluster__resolved_mappings = Slot(
    uri=MCLUSTER.resolved_mappings,
    name="mappingCluster__resolved_mappings",
    curie=MCLUSTER.curie("resolved_mappings"),
    model_uri=MCLUSTER.mappingCluster__resolved_mappings,
    domain=None,
    range=Optional[Union[Union[dict, SimpleMapping], List[Union[dict, SimpleMapping]]]],
)

slots.mappingCluster__input_mappings = Slot(
    uri=MCLUSTER.input_mappings,
    name="mappingCluster__input_mappings",
    curie=MCLUSTER.curie("input_mappings"),
    model_uri=MCLUSTER.mappingCluster__input_mappings,
    domain=None,
    range=Optional[Union[Union[dict, SimpleMapping], List[Union[dict, SimpleMapping]]]],
)

slots.mappingCluster__subsequent_raw_scores = Slot(
    uri=MCLUSTER.subsequent_raw_scores,
    name="mappingCluster__subsequent_raw_scores",
    curie=MCLUSTER.curie("subsequent_raw_scores"),
    model_uri=MCLUSTER.mappingCluster__subsequent_raw_scores,
    domain=None,
    range=Optional[Union[float, List[float]]],
)

slots.mappingCluster__depiction = Slot(
    uri=MCLUSTER.depiction,
    name="mappingCluster__depiction",
    curie=MCLUSTER.curie("depiction"),
    model_uri=MCLUSTER.mappingCluster__depiction,
    domain=None,
    range=Optional[Union[str, ImageLocation]],
)

slots.mappingCluster__data_objects = Slot(
    uri=MCLUSTER.data_objects,
    name="mappingCluster__data_objects",
    curie=MCLUSTER.curie("data_objects"),
    model_uri=MCLUSTER.mappingCluster__data_objects,
    domain=None,
    range=Optional[Union[str, DataObjectLocation]],
)

slots.simpleMapping__cluster_id = Slot(
    uri=MCLUSTER.cluster_id,
    name="simpleMapping__cluster_id",
    curie=MCLUSTER.curie("cluster_id"),
    model_uri=MCLUSTER.simpleMapping__cluster_id,
    domain=None,
    range=Optional[Union[str, MappingClusterId]],
)

slots.simpleMapping__subject_id = Slot(
    uri=SSSOM.subject_id,
    name="simpleMapping__subject_id",
    curie=SSSOM.curie("subject_id"),
    model_uri=MCLUSTER.simpleMapping__subject_id,
    domain=None,
    range=Optional[str],
)

slots.simpleMapping__subject_label = Slot(
    uri=SSSOM.subject_label,
    name="simpleMapping__subject_label",
    curie=SSSOM.curie("subject_label"),
    model_uri=MCLUSTER.simpleMapping__subject_label,
    domain=None,
    range=Optional[str],
)

slots.simpleMapping__predicate_id = Slot(
    uri=SSSOM.predicate_id,
    name="simpleMapping__predicate_id",
    curie=SSSOM.curie("predicate_id"),
    model_uri=MCLUSTER.simpleMapping__predicate_id,
    domain=None,
    range=Optional[str],
)

slots.simpleMapping__predicate_label = Slot(
    uri=SSSOM.predicate_label,
    name="simpleMapping__predicate_label",
    curie=SSSOM.curie("predicate_label"),
    model_uri=MCLUSTER.simpleMapping__predicate_label,
    domain=None,
    range=Optional[str],
)

slots.simpleMapping__object_id = Slot(
    uri=SSSOM.object_id,
    name="simpleMapping__object_id",
    curie=SSSOM.curie("object_id"),
    model_uri=MCLUSTER.simpleMapping__object_id,
    domain=None,
    range=Optional[str],
)

slots.simpleMapping__object_label = Slot(
    uri=SSSOM.object_label,
    name="simpleMapping__object_label",
    curie=SSSOM.curie("object_label"),
    model_uri=MCLUSTER.simpleMapping__object_label,
    domain=None,
    range=Optional[str],
)

slots.simpleMapping__is_most_probable = Slot(
    uri=MCLUSTER.is_most_probable,
    name="simpleMapping__is_most_probable",
    curie=MCLUSTER.curie("is_most_probable"),
    model_uri=MCLUSTER.simpleMapping__is_most_probable,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.simpleMapping__prior_probability = Slot(
    uri=MCLUSTER.prior_probability,
    name="simpleMapping__prior_probability",
    curie=MCLUSTER.curie("prior_probability"),
    model_uri=MCLUSTER.simpleMapping__prior_probability,
    domain=None,
    range=Optional[Union[float, Probability]],
)

slots.simpleMapping__posterior_probability = Slot(
    uri=MCLUSTER.posterior_probability,
    name="simpleMapping__posterior_probability",
    curie=MCLUSTER.curie("posterior_probability"),
    model_uri=MCLUSTER.simpleMapping__posterior_probability,
    domain=None,
    range=Optional[Union[float, Probability]],
)

slots.simpleMapping__predicate_probabilities = Slot(
    uri=MCLUSTER.predicate_probabilities,
    name="simpleMapping__predicate_probabilities",
    curie=MCLUSTER.curie("predicate_probabilities"),
    model_uri=MCLUSTER.simpleMapping__predicate_probabilities,
    domain=None,
    range=Optional[
        Union[
            Union[str, PredicateProbabilityPredicateId],
            List[Union[str, PredicateProbabilityPredicateId]],
        ]
    ],
)

slots.simpleMapping__confidence = Slot(
    uri=MCLUSTER.confidence,
    name="simpleMapping__confidence",
    curie=MCLUSTER.curie("confidence"),
    model_uri=MCLUSTER.simpleMapping__confidence,
    domain=None,
    range=Optional[Union[float, Probability]],
)

slots.predicateProbability__predicate_id = Slot(
    uri=MCLUSTER.predicate_id,
    name="predicateProbability__predicate_id",
    curie=MCLUSTER.curie("predicate_id"),
    model_uri=MCLUSTER.predicateProbability__predicate_id,
    domain=None,
    range=URIRef,
)

slots.predicateProbability__probability = Slot(
    uri=MCLUSTER.probability,
    name="predicateProbability__probability",
    curie=MCLUSTER.curie("probability"),
    model_uri=MCLUSTER.predicateProbability__probability,
    domain=None,
    range=Optional[Union[float, Probability]],
)

slots.lexicalIndex__groupings = Slot(
    uri=MCLUSTER.groupings,
    name="lexicalIndex__groupings",
    curie=MCLUSTER.curie("groupings"),
    model_uri=MCLUSTER.lexicalIndex__groupings,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, LexicalGroupingTerm], Union[dict, LexicalGrouping]],
            List[Union[dict, LexicalGrouping]],
        ]
    ],
)

slots.lexicalIndex__pipelines = Slot(
    uri=MCLUSTER.pipelines,
    name="lexicalIndex__pipelines",
    curie=MCLUSTER.curie("pipelines"),
    model_uri=MCLUSTER.lexicalIndex__pipelines,
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
    uri=MCLUSTER.term,
    name="lexicalGrouping__term",
    curie=MCLUSTER.curie("term"),
    model_uri=MCLUSTER.lexicalGrouping__term,
    domain=None,
    range=URIRef,
)

slots.lexicalGrouping__relationships = Slot(
    uri=MCLUSTER.relationships,
    name="lexicalGrouping__relationships",
    curie=MCLUSTER.curie("relationships"),
    model_uri=MCLUSTER.lexicalGrouping__relationships,
    domain=None,
    range=Optional[Union[Union[dict, RelationshipToTerm], List[Union[dict, RelationshipToTerm]]]],
)

slots.relationshipToTerm__predicate = Slot(
    uri=MCLUSTER.predicate,
    name="relationshipToTerm__predicate",
    curie=MCLUSTER.curie("predicate"),
    model_uri=MCLUSTER.relationshipToTerm__predicate,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.relationshipToTerm__element = Slot(
    uri=MCLUSTER.element,
    name="relationshipToTerm__element",
    curie=MCLUSTER.curie("element"),
    model_uri=MCLUSTER.relationshipToTerm__element,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.relationshipToTerm__element_term = Slot(
    uri=MCLUSTER.element_term,
    name="relationshipToTerm__element_term",
    curie=MCLUSTER.curie("element_term"),
    model_uri=MCLUSTER.relationshipToTerm__element_term,
    domain=None,
    range=Optional[str],
)

slots.relationshipToTerm__source = Slot(
    uri=MCLUSTER.source,
    name="relationshipToTerm__source",
    curie=MCLUSTER.curie("source"),
    model_uri=MCLUSTER.relationshipToTerm__source,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.relationshipToTerm__pipeline = Slot(
    uri=MCLUSTER.pipeline,
    name="relationshipToTerm__pipeline",
    curie=MCLUSTER.curie("pipeline"),
    model_uri=MCLUSTER.relationshipToTerm__pipeline,
    domain=None,
    range=Optional[
        Union[
            Union[str, LexicalTransformationPipelineName],
            List[Union[str, LexicalTransformationPipelineName]],
        ]
    ],
)

slots.relationshipToTerm__synonymized = Slot(
    uri=MCLUSTER.synonymized,
    name="relationshipToTerm__synonymized",
    curie=MCLUSTER.curie("synonymized"),
    model_uri=MCLUSTER.relationshipToTerm__synonymized,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.lexicalTransformationPipeline__name = Slot(
    uri=MCLUSTER.name,
    name="lexicalTransformationPipeline__name",
    curie=MCLUSTER.curie("name"),
    model_uri=MCLUSTER.lexicalTransformationPipeline__name,
    domain=None,
    range=URIRef,
)

slots.lexicalTransformationPipeline__transformations = Slot(
    uri=MCLUSTER.transformations,
    name="lexicalTransformationPipeline__transformations",
    curie=MCLUSTER.curie("transformations"),
    model_uri=MCLUSTER.lexicalTransformationPipeline__transformations,
    domain=None,
    range=Optional[
        Union[Union[dict, LexicalTransformation], List[Union[dict, LexicalTransformation]]]
    ],
)

slots.lexicalTransformation__type = Slot(
    uri=MCLUSTER.type,
    name="lexicalTransformation__type",
    curie=MCLUSTER.curie("type"),
    model_uri=MCLUSTER.lexicalTransformation__type,
    domain=None,
    range=Optional[Union[str, "TransformationType"]],
)

slots.lexicalTransformation__params = Slot(
    uri=MCLUSTER.params,
    name="lexicalTransformation__params",
    curie=MCLUSTER.curie("params"),
    model_uri=MCLUSTER.lexicalTransformation__params,
    domain=None,
    range=Optional[str],
)
