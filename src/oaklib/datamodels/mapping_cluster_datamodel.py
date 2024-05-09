# Auto generated from mapping_cluster_datamodel.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-02-27T10:04:41
# Schema: mapping-cluster-datamodel
#
# id: https://w3id.org/oak/mapping-cluster-datamodel
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
from linkml_runtime.linkml_model.types import Boolean, Datetime, Float, String
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import (
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
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
MCLUSTER = CurieNamespace("mcluster", "https://w3id.org/oak/mapping-cluster-datamodel/")
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
            (
                v
                if isinstance(v, PredicateProbabilityPredicateId)
                else PredicateProbabilityPredicateId(v)
            )
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


# Enumerations
class MappingConcordanceEnum(EnumDefinitionImpl):
    """
    The degree to which a mapping interpreted in light of a mapping cluster is consistent with the input mappings
    """

    NEW = PermissibleValue(
        text="NEW", description="this mapping interpretation can be added with high confidence"
    )
    AMBIGUOUS = PermissibleValue(
        text="AMBIGUOUS",
        description="the source ontology has different interpretations (e.g. exact, broad) for the same term pair. If you get this then you should tidy up your inputs",
    )
    CONFLICT = PermissibleValue(
        text="CONFLICT",
        description="the source ontology mapping interpretation is different from what is inferred to be the correct one",
    )
    REJECT = PermissibleValue(
        text="REJECT", description="a CONFLICT in which the source interpretation is non-exact"
    )

    _defn = EnumDefinition(
        name="MappingConcordanceEnum",
        description="The degree to which a mapping interpreted in light of a mapping cluster is consistent with the input mappings",
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
