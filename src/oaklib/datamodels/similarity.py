# Auto generated from similarity.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-05-13T10:39:24
# Schema: similarity
#
# id: https://w3id.org/linkml/similarity
# description: A datamodel for representing similarity between terms or lists of terms.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from linkml_runtime.linkml_model.types import Float, Integer
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.metamodelcore import URIorCURIE
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
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SIM = CurieNamespace("sim", "https://w3id.org/linkml/similarity/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
SSSOM = CurieNamespace("sssom", "http://w3id.org/sssom/")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = SIM


# Types
class ZeroToOne(Float):
    type_class_uri = XSD.float
    type_class_curie = "xsd:float"
    type_name = "ZeroToOne"
    type_model_uri = SIM.ZeroToOne


class NonNegativeFloat(Float):
    type_class_uri = XSD.float
    type_class_curie = "xsd:float"
    type_name = "NonNegativeFloat"
    type_model_uri = SIM.NonNegativeFloat


class NegativeLogValue(Float):
    type_class_uri = XSD.float
    type_class_curie = "xsd:float"
    type_name = "NegativeLogValue"
    type_model_uri = SIM.NegativeLogValue


class ItemCount(Integer):
    type_class_uri = XSD.integer
    type_class_curie = "xsd:integer"
    type_name = "ItemCount"
    type_model_uri = SIM.ItemCount


# Class references


@dataclass
class PairwiseSimilarity(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SIM.PairwiseSimilarity
    class_class_curie: ClassVar[str] = "sim:PairwiseSimilarity"
    class_name: ClassVar[str] = "PairwiseSimilarity"
    class_model_uri: ClassVar[URIRef] = SIM.PairwiseSimilarity

    subject_id: Optional[Union[str, URIorCURIE]] = None
    subject_label: Optional[str] = None
    subject_source: Optional[str] = None
    object_id: Optional[Union[str, URIorCURIE]] = None
    object_label: Optional[str] = None
    object_source: Optional[str] = None
    ancestor_id: Optional[Union[str, URIorCURIE]] = None
    ancestor_label: Optional[str] = None
    ancestor_source: Optional[str] = None
    object_information_content: Optional[Union[float, NegativeLogValue]] = None
    subject_information_content: Optional[Union[float, NegativeLogValue]] = None
    ancestor_information_content: Optional[Union[float, NegativeLogValue]] = None
    jaccard_similarity: Optional[Union[float, ZeroToOne]] = None
    dice_similarity: Optional[Union[float, ZeroToOne]] = None
    phenodigm_score: Optional[Union[float, NonNegativeFloat]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.subject_id is not None and not isinstance(self.subject_id, URIorCURIE):
            self.subject_id = URIorCURIE(self.subject_id)

        if self.subject_label is not None and not isinstance(self.subject_label, str):
            self.subject_label = str(self.subject_label)

        if self.subject_source is not None and not isinstance(self.subject_source, str):
            self.subject_source = str(self.subject_source)

        if self.object_id is not None and not isinstance(self.object_id, URIorCURIE):
            self.object_id = URIorCURIE(self.object_id)

        if self.object_label is not None and not isinstance(self.object_label, str):
            self.object_label = str(self.object_label)

        if self.object_source is not None and not isinstance(self.object_source, str):
            self.object_source = str(self.object_source)

        if self.ancestor_id is not None and not isinstance(self.ancestor_id, URIorCURIE):
            self.ancestor_id = URIorCURIE(self.ancestor_id)

        if self.ancestor_label is not None and not isinstance(self.ancestor_label, str):
            self.ancestor_label = str(self.ancestor_label)

        if self.ancestor_source is not None and not isinstance(self.ancestor_source, str):
            self.ancestor_source = str(self.ancestor_source)

        if self.object_information_content is not None and not isinstance(
            self.object_information_content, NegativeLogValue
        ):
            self.object_information_content = NegativeLogValue(self.object_information_content)

        if self.subject_information_content is not None and not isinstance(
            self.subject_information_content, NegativeLogValue
        ):
            self.subject_information_content = NegativeLogValue(self.subject_information_content)

        if self.ancestor_information_content is not None and not isinstance(
            self.ancestor_information_content, NegativeLogValue
        ):
            self.ancestor_information_content = NegativeLogValue(self.ancestor_information_content)

        if self.jaccard_similarity is not None and not isinstance(
            self.jaccard_similarity, ZeroToOne
        ):
            self.jaccard_similarity = ZeroToOne(self.jaccard_similarity)

        if self.dice_similarity is not None and not isinstance(self.dice_similarity, ZeroToOne):
            self.dice_similarity = ZeroToOne(self.dice_similarity)

        if self.phenodigm_score is not None and not isinstance(
            self.phenodigm_score, NonNegativeFloat
        ):
            self.phenodigm_score = NonNegativeFloat(self.phenodigm_score)

        super().__post_init__(**kwargs)


class TermPairwiseSimilarity(PairwiseSimilarity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SIM.TermPairwiseSimilarity
    class_class_curie: ClassVar[str] = "sim:TermPairwiseSimilarity"
    class_name: ClassVar[str] = "TermPairwiseSimilarity"
    class_model_uri: ClassVar[URIRef] = SIM.TermPairwiseSimilarity


class TermSetPairwiseSimilarity(PairwiseSimilarity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SIM.TermSetPairwiseSimilarity
    class_class_curie: ClassVar[str] = "sim:TermSetPairwiseSimilarity"
    class_name: ClassVar[str] = "TermSetPairwiseSimilarity"
    class_model_uri: ClassVar[URIRef] = SIM.TermSetPairwiseSimilarity


# Enumerations


# Slots
class slots:
    pass


slots.subject_id = Slot(
    uri=SSSOM.subject_id,
    name="subject_id",
    curie=SSSOM.curie("subject_id"),
    model_uri=SIM.subject_id,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.subject_label = Slot(
    uri=SSSOM.subject_label,
    name="subject_label",
    curie=SSSOM.curie("subject_label"),
    model_uri=SIM.subject_label,
    domain=None,
    range=Optional[str],
)

slots.subject_source = Slot(
    uri=SSSOM.subject_source,
    name="subject_source",
    curie=SSSOM.curie("subject_source"),
    model_uri=SIM.subject_source,
    domain=None,
    range=Optional[str],
)

slots.object_id = Slot(
    uri=SSSOM.object_id,
    name="object_id",
    curie=SSSOM.curie("object_id"),
    model_uri=SIM.object_id,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.object_label = Slot(
    uri=SSSOM.object_label,
    name="object_label",
    curie=SSSOM.curie("object_label"),
    model_uri=SIM.object_label,
    domain=None,
    range=Optional[str],
)

slots.object_source = Slot(
    uri=SSSOM.object_source,
    name="object_source",
    curie=SSSOM.curie("object_source"),
    model_uri=SIM.object_source,
    domain=None,
    range=Optional[str],
)

slots.ancestor_id = Slot(
    uri=SIM.ancestor_id,
    name="ancestor_id",
    curie=SIM.curie("ancestor_id"),
    model_uri=SIM.ancestor_id,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.ancestor_label = Slot(
    uri=SIM.ancestor_label,
    name="ancestor_label",
    curie=SIM.curie("ancestor_label"),
    model_uri=SIM.ancestor_label,
    domain=None,
    range=Optional[str],
)

slots.ancestor_source = Slot(
    uri=SIM.ancestor_source,
    name="ancestor_source",
    curie=SIM.curie("ancestor_source"),
    model_uri=SIM.ancestor_source,
    domain=None,
    range=Optional[str],
)

slots.score = Slot(
    uri=SIM.score,
    name="score",
    curie=SIM.curie("score"),
    model_uri=SIM.score,
    domain=None,
    range=Optional[str],
)

slots.information_content = Slot(
    uri=SIM.information_content,
    name="information_content",
    curie=SIM.curie("information_content"),
    model_uri=SIM.information_content,
    domain=None,
    range=Optional[Union[float, NegativeLogValue]],
)

slots.subject_information_content = Slot(
    uri=SIM.subject_information_content,
    name="subject_information_content",
    curie=SIM.curie("subject_information_content"),
    model_uri=SIM.subject_information_content,
    domain=None,
    range=Optional[Union[float, NegativeLogValue]],
)

slots.object_information_content = Slot(
    uri=SIM.object_information_content,
    name="object_information_content",
    curie=SIM.curie("object_information_content"),
    model_uri=SIM.object_information_content,
    domain=None,
    range=Optional[Union[float, NegativeLogValue]],
)

slots.ancestor_information_content = Slot(
    uri=SIM.ancestor_information_content,
    name="ancestor_information_content",
    curie=SIM.curie("ancestor_information_content"),
    model_uri=SIM.ancestor_information_content,
    domain=None,
    range=Optional[Union[float, NegativeLogValue]],
)

slots.jaccard_similarity = Slot(
    uri=SIM.jaccard_similarity,
    name="jaccard_similarity",
    curie=SIM.curie("jaccard_similarity"),
    model_uri=SIM.jaccard_similarity,
    domain=None,
    range=Optional[Union[float, ZeroToOne]],
)

slots.dice_similarity = Slot(
    uri=SIM.dice_similarity,
    name="dice_similarity",
    curie=SIM.curie("dice_similarity"),
    model_uri=SIM.dice_similarity,
    domain=None,
    range=Optional[Union[float, ZeroToOne]],
)

slots.phenodigm_score = Slot(
    uri=SIM.phenodigm_score,
    name="phenodigm_score",
    curie=SIM.curie("phenodigm_score"),
    model_uri=SIM.phenodigm_score,
    domain=None,
    range=Optional[Union[float, NonNegativeFloat]],
)

slots.overlap_coefficient = Slot(
    uri=SIM.overlap_coefficient,
    name="overlap_coefficient",
    curie=SIM.curie("overlap_coefficient"),
    model_uri=SIM.overlap_coefficient,
    domain=None,
    range=Optional[Union[float, ZeroToOne]],
)

slots.subsumes_score = Slot(
    uri=SIM.subsumes_score,
    name="subsumes_score",
    curie=SIM.curie("subsumes_score"),
    model_uri=SIM.subsumes_score,
    domain=None,
    range=Optional[Union[float, ZeroToOne]],
)

slots.subsumed_by_score = Slot(
    uri=SIM.subsumed_by_score,
    name="subsumed_by_score",
    curie=SIM.curie("subsumed_by_score"),
    model_uri=SIM.subsumed_by_score,
    domain=None,
    range=Optional[Union[float, ZeroToOne]],
)

slots.intersection_count = Slot(
    uri=SIM.intersection_count,
    name="intersection_count",
    curie=SIM.curie("intersection_count"),
    model_uri=SIM.intersection_count,
    domain=None,
    range=Optional[Union[int, ItemCount]],
)

slots.union_count = Slot(
    uri=SIM.union_count,
    name="union_count",
    curie=SIM.curie("union_count"),
    model_uri=SIM.union_count,
    domain=None,
    range=Optional[Union[int, ItemCount]],
)
