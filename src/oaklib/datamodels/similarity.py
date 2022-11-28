# Auto generated from similarity.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-09-07T23:25:27
# Schema: similarity
#
# id: https://w3id.org/linkml/similarity
# description: A datamodel for representing semantic similarity between terms or lists of terms.
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
from linkml_runtime.linkml_model.types import Float, Integer, String, Uriorcurie
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import URIorCURIE, bnode, empty_dict, empty_list
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
class TermInfoId(extended_str):
    pass


class BestMatchMatchSource(extended_str):
    pass


class PairwiseSimilarity(YAMLRoot):
    """
    Abstract grouping for representing individual pairwise similarities
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SIM.PairwiseSimilarity
    class_class_curie: ClassVar[str] = "sim:PairwiseSimilarity"
    class_name: ClassVar[str] = "PairwiseSimilarity"
    class_model_uri: ClassVar[URIRef] = SIM.PairwiseSimilarity


@dataclass
class TermPairwiseSimilarity(PairwiseSimilarity):
    """
    A simple pairwise similarity between two atomic concepts/terms
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SIM.TermPairwiseSimilarity
    class_class_curie: ClassVar[str] = "sim:TermPairwiseSimilarity"
    class_name: ClassVar[str] = "TermPairwiseSimilarity"
    class_model_uri: ClassVar[URIRef] = SIM.TermPairwiseSimilarity

    subject_id: Union[str, URIorCURIE] = None
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
        if self._is_empty(self.subject_id):
            self.MissingRequiredField("subject_id")
        if not isinstance(self.subject_id, URIorCURIE):
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


@dataclass
class TermSetPairwiseSimilarity(PairwiseSimilarity):
    """
    A simple pairwise similarity between two sets of concepts/terms
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SIM.TermSetPairwiseSimilarity
    class_class_curie: ClassVar[str] = "sim:TermSetPairwiseSimilarity"
    class_name: ClassVar[str] = "TermSetPairwiseSimilarity"
    class_model_uri: ClassVar[URIRef] = SIM.TermSetPairwiseSimilarity

    subject_termset: Optional[
        Union[Dict[Union[str, TermInfoId], Union[dict, "TermInfo"]], List[Union[dict, "TermInfo"]]]
    ] = empty_dict()
    object_termset: Optional[
        Union[Dict[Union[str, TermInfoId], Union[dict, "TermInfo"]], List[Union[dict, "TermInfo"]]]
    ] = empty_dict()
    subject_best_matches: Optional[
        Union[
            Dict[Union[str, BestMatchMatchSource], Union[dict, "BestMatch"]],
            List[Union[dict, "BestMatch"]],
        ]
    ] = empty_dict()
    object_best_matches: Optional[
        Union[
            Dict[Union[str, BestMatchMatchSource], Union[dict, "BestMatch"]],
            List[Union[dict, "BestMatch"]],
        ]
    ] = empty_dict()
    average_score: Optional[float] = None
    best_score: Optional[float] = None
    metric: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(
            slot_name="subject_termset", slot_type=TermInfo, key_name="id", keyed=True
        )

        self._normalize_inlined_as_dict(
            slot_name="object_termset", slot_type=TermInfo, key_name="id", keyed=True
        )

        self._normalize_inlined_as_dict(
            slot_name="subject_best_matches",
            slot_type=BestMatch,
            key_name="match_source",
            keyed=True,
        )

        self._normalize_inlined_as_dict(
            slot_name="object_best_matches",
            slot_type=BestMatch,
            key_name="match_source",
            keyed=True,
        )

        if self.average_score is not None and not isinstance(self.average_score, float):
            self.average_score = float(self.average_score)

        if self.best_score is not None and not isinstance(self.best_score, float):
            self.best_score = float(self.best_score)

        if self.metric is not None and not isinstance(self.metric, URIorCURIE):
            self.metric = URIorCURIE(self.metric)

        super().__post_init__(**kwargs)


@dataclass
class TermInfo(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SIM.TermInfo
    class_class_curie: ClassVar[str] = "sim:TermInfo"
    class_name: ClassVar[str] = "TermInfo"
    class_model_uri: ClassVar[URIRef] = SIM.TermInfo

    id: Union[str, TermInfoId] = None
    label: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TermInfoId):
            self.id = TermInfoId(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass
class BestMatch(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SIM.BestMatch
    class_class_curie: ClassVar[str] = "sim:BestMatch"
    class_name: ClassVar[str] = "BestMatch"
    class_model_uri: ClassVar[URIRef] = SIM.BestMatch

    match_source: Union[str, BestMatchMatchSource] = None
    match_source_label: Optional[str] = None
    match_target: Optional[str] = None
    match_target_label: Optional[str] = None
    score: Optional[float] = None
    match_subsumer: Optional[Union[str, URIorCURIE]] = None
    match_subsumer_label: Optional[str] = None
    similarity: Optional[Union[dict, TermPairwiseSimilarity]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.match_source):
            self.MissingRequiredField("match_source")
        if not isinstance(self.match_source, BestMatchMatchSource):
            self.match_source = BestMatchMatchSource(self.match_source)

        if self.match_source_label is not None and not isinstance(self.match_source_label, str):
            self.match_source_label = str(self.match_source_label)

        if self.match_target is not None and not isinstance(self.match_target, str):
            self.match_target = str(self.match_target)

        if self.match_target_label is not None and not isinstance(self.match_target_label, str):
            self.match_target_label = str(self.match_target_label)

        if self.score is not None and not isinstance(self.score, float):
            self.score = float(self.score)

        if self.match_subsumer is not None and not isinstance(self.match_subsumer, URIorCURIE):
            self.match_subsumer = URIorCURIE(self.match_subsumer)

        if self.match_subsumer_label is not None and not isinstance(self.match_subsumer_label, str):
            self.match_subsumer_label = str(self.match_subsumer_label)

        if self.similarity is not None and not isinstance(self.similarity, TermPairwiseSimilarity):
            self.similarity = TermPairwiseSimilarity(**as_dict(self.similarity))

        super().__post_init__(**kwargs)


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
    range=Union[str, URIorCURIE],
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

slots.subject_termset = Slot(
    uri=SIM.subject_termset,
    name="subject_termset",
    curie=SIM.curie("subject_termset"),
    model_uri=SIM.subject_termset,
    domain=None,
    range=Optional[
        Union[Dict[Union[str, TermInfoId], Union[dict, TermInfo]], List[Union[dict, TermInfo]]]
    ],
)

slots.object_termset = Slot(
    uri=SIM.object_termset,
    name="object_termset",
    curie=SIM.curie("object_termset"),
    model_uri=SIM.object_termset,
    domain=None,
    range=Optional[
        Union[Dict[Union[str, TermInfoId], Union[dict, TermInfo]], List[Union[dict, TermInfo]]]
    ],
)

slots.subject_best_matches = Slot(
    uri=SIM.subject_best_matches,
    name="subject_best_matches",
    curie=SIM.curie("subject_best_matches"),
    model_uri=SIM.subject_best_matches,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, BestMatchMatchSource], Union[dict, BestMatch]],
            List[Union[dict, BestMatch]],
        ]
    ],
)

slots.object_best_matches = Slot(
    uri=SIM.object_best_matches,
    name="object_best_matches",
    curie=SIM.curie("object_best_matches"),
    model_uri=SIM.object_best_matches,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, BestMatchMatchSource], Union[dict, BestMatch]],
            List[Union[dict, BestMatch]],
        ]
    ],
)

slots.metric = Slot(
    uri=SIM.metric,
    name="metric",
    curie=SIM.curie("metric"),
    model_uri=SIM.metric,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.average_score = Slot(
    uri=SIM.average_score,
    name="average_score",
    curie=SIM.curie("average_score"),
    model_uri=SIM.average_score,
    domain=None,
    range=Optional[float],
)

slots.best_score = Slot(
    uri=SIM.best_score,
    name="best_score",
    curie=SIM.curie("best_score"),
    model_uri=SIM.best_score,
    domain=None,
    range=Optional[float],
)

slots.termInfo__id = Slot(
    uri=SIM.id,
    name="termInfo__id",
    curie=SIM.curie("id"),
    model_uri=SIM.termInfo__id,
    domain=None,
    range=URIRef,
)

slots.termInfo__label = Slot(
    uri=RDFS.label,
    name="termInfo__label",
    curie=RDFS.curie("label"),
    model_uri=SIM.termInfo__label,
    domain=None,
    range=Optional[str],
)

slots.bestMatch__match_source = Slot(
    uri=SIM.match_source,
    name="bestMatch__match_source",
    curie=SIM.curie("match_source"),
    model_uri=SIM.bestMatch__match_source,
    domain=None,
    range=URIRef,
)

slots.bestMatch__match_source_label = Slot(
    uri=SIM.match_source_label,
    name="bestMatch__match_source_label",
    curie=SIM.curie("match_source_label"),
    model_uri=SIM.bestMatch__match_source_label,
    domain=None,
    range=Optional[str],
)

slots.bestMatch__match_target = Slot(
    uri=SIM.match_target,
    name="bestMatch__match_target",
    curie=SIM.curie("match_target"),
    model_uri=SIM.bestMatch__match_target,
    domain=None,
    range=Optional[str],
)

slots.bestMatch__match_target_label = Slot(
    uri=SIM.match_target_label,
    name="bestMatch__match_target_label",
    curie=SIM.curie("match_target_label"),
    model_uri=SIM.bestMatch__match_target_label,
    domain=None,
    range=Optional[str],
)

slots.bestMatch__score = Slot(
    uri=SIM.score,
    name="bestMatch__score",
    curie=SIM.curie("score"),
    model_uri=SIM.bestMatch__score,
    domain=None,
    range=Optional[float],
)

slots.bestMatch__match_subsumer = Slot(
    uri=SIM.match_subsumer,
    name="bestMatch__match_subsumer",
    curie=SIM.curie("match_subsumer"),
    model_uri=SIM.bestMatch__match_subsumer,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.bestMatch__match_subsumer_label = Slot(
    uri=SIM.match_subsumer_label,
    name="bestMatch__match_subsumer_label",
    curie=SIM.curie("match_subsumer_label"),
    model_uri=SIM.bestMatch__match_subsumer_label,
    domain=None,
    range=Optional[str],
)

slots.bestMatch__similarity = Slot(
    uri=SIM.similarity,
    name="bestMatch__similarity",
    curie=SIM.curie("similarity"),
    model_uri=SIM.bestMatch__similarity,
    domain=None,
    range=Optional[Union[dict, TermPairwiseSimilarity]],
)
