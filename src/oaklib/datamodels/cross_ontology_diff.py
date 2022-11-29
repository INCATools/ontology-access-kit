# Auto generated from cross_ontology_diff.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-07-10T18:38:16
# Schema: cross-ontology-diff
#
# id: https://w3id.org/linkml/cross_ontology_diff
# description: A datamodel for representing the results of relational diffs across a pair of ontologies connected
#              by mappings
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
ANN = CurieNamespace("ann", "https://w3id.org/linkml/text_annotator/")
BPA = CurieNamespace("bpa", "https://bioportal.bioontology.org/annotator/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
PAV = CurieNamespace("pav", "http://purl.org/pav/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
SSSOM = CurieNamespace("sssom", "http://w3id.org/sssom/")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = ANN


# Types
class Label(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "Label"
    type_model_uri = ANN.Label


class EntityReference(Uriorcurie):
    """A reference to a mapped entity. This is represented internally as a string, and as a resource in RDF"""

    type_class_uri = RDFS.Resource
    type_class_curie = "rdfs:Resource"
    type_name = "EntityReference"
    type_model_uri = ANN.EntityReference


# Class references


@dataclass
class StructureDiffResultSet(YAMLRoot):
    """
    A collection of relational diff results results
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ANN.StructureDiffResultSet
    class_class_curie: ClassVar[str] = "ann:StructureDiffResultSet"
    class_name: ClassVar[str] = "StructureDiffResultSet"
    class_model_uri: ClassVar[URIRef] = ANN.StructureDiffResultSet

    results: Optional[
        Union[Union[dict, "RelationalDiff"], List[Union[dict, "RelationalDiff"]]]
    ] = empty_list()
    left_source: Optional[str] = None
    right_source: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(
            slot_name="results", slot_type=RelationalDiff, key_name="left_subject_id", keyed=False
        )

        if self.left_source is not None and not isinstance(self.left_source, str):
            self.left_source = str(self.left_source)

        if self.right_source is not None and not isinstance(self.right_source, str):
            self.right_source = str(self.right_source)

        super().__post_init__(**kwargs)


@dataclass
class RelationalDiff(YAMLRoot):
    """
    A relational diff expresses the difference between an edge in one ontology, and an edge (or lack of edge) in
    another ontology (or a different version of the same ontology). The diff is from the perspective of one
    ontology (the one on the "left" side).

    For every edge in the left ontology, the subject and object are mapped to the right ontology.
    If mappings cannot be found then the diff is categorized as missing mappings.
    The predicate is also mapped, with the reflexivity assumption.

    for every mapped subject and object pair (the "right" subject and object), the entailed relationship
    is examined to determine if it consistent with the left predicate.

    ```
    left_object    <--- mapped to ---> right_object
    ^                                  ^
    |                                  |
    |                                  |
    | left                             | right
    | predicate                        | predicate
    |                                  |
    |                                  |
    left_subject   <--- mapped to ---> right_subject
    ```
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ANN.RelationalDiff
    class_class_curie: ClassVar[str] = "ann:RelationalDiff"
    class_name: ClassVar[str] = "RelationalDiff"
    class_model_uri: ClassVar[URIRef] = ANN.RelationalDiff

    left_subject_id: Union[str, EntityReference] = None
    left_object_id: Union[str, EntityReference] = None
    left_predicate_id: Union[str, EntityReference] = None
    category: Optional[Union[str, "DiffCategory"]] = None
    left_subject_label: Optional[Union[str, Label]] = None
    left_object_label: Optional[Union[str, Label]] = None
    left_predicate_label: Optional[Union[str, Label]] = None
    right_subject_id: Optional[Union[str, EntityReference]] = None
    right_object_id: Optional[Union[str, EntityReference]] = None
    right_predicate_ids: Optional[
        Union[Union[str, EntityReference], List[Union[str, EntityReference]]]
    ] = empty_list()
    right_subject_label: Optional[Union[str, Label]] = None
    right_object_label: Optional[Union[str, Label]] = None
    right_predicate_labels: Optional[
        Union[Union[str, Label], List[Union[str, Label]]]
    ] = empty_list()
    left_subject_is_functional: Optional[str] = None
    left_object_is_functional: Optional[str] = None
    subject_mapping_predicate: Optional[Union[str, EntityReference]] = None
    object_mapping_predicate: Optional[Union[str, EntityReference]] = None
    right_intermediate_ids: Optional[
        Union[Union[str, EntityReference], List[Union[str, EntityReference]]]
    ] = empty_list()
    subject_mapping_cardinality: Optional[Union[str, "MappingCardinalityEnum"]] = None
    object_mapping_cardinality: Optional[Union[str, "MappingCardinalityEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.left_subject_id):
            self.MissingRequiredField("left_subject_id")
        if not isinstance(self.left_subject_id, EntityReference):
            self.left_subject_id = EntityReference(self.left_subject_id)

        if self._is_empty(self.left_object_id):
            self.MissingRequiredField("left_object_id")
        if not isinstance(self.left_object_id, EntityReference):
            self.left_object_id = EntityReference(self.left_object_id)

        if self._is_empty(self.left_predicate_id):
            self.MissingRequiredField("left_predicate_id")
        if not isinstance(self.left_predicate_id, EntityReference):
            self.left_predicate_id = EntityReference(self.left_predicate_id)

        if self.category is not None and not isinstance(self.category, DiffCategory):
            self.category = DiffCategory(self.category)

        if self.left_subject_label is not None and not isinstance(self.left_subject_label, Label):
            self.left_subject_label = Label(self.left_subject_label)

        if self.left_object_label is not None and not isinstance(self.left_object_label, Label):
            self.left_object_label = Label(self.left_object_label)

        if self.left_predicate_label is not None and not isinstance(
            self.left_predicate_label, Label
        ):
            self.left_predicate_label = Label(self.left_predicate_label)

        if self.right_subject_id is not None and not isinstance(
            self.right_subject_id, EntityReference
        ):
            self.right_subject_id = EntityReference(self.right_subject_id)

        if self.right_object_id is not None and not isinstance(
            self.right_object_id, EntityReference
        ):
            self.right_object_id = EntityReference(self.right_object_id)

        if not isinstance(self.right_predicate_ids, list):
            self.right_predicate_ids = (
                [self.right_predicate_ids] if self.right_predicate_ids is not None else []
            )
        self.right_predicate_ids = [
            v if isinstance(v, EntityReference) else EntityReference(v)
            for v in self.right_predicate_ids
        ]

        if self.right_subject_label is not None and not isinstance(self.right_subject_label, Label):
            self.right_subject_label = Label(self.right_subject_label)

        if self.right_object_label is not None and not isinstance(self.right_object_label, Label):
            self.right_object_label = Label(self.right_object_label)

        if not isinstance(self.right_predicate_labels, list):
            self.right_predicate_labels = (
                [self.right_predicate_labels] if self.right_predicate_labels is not None else []
            )
        self.right_predicate_labels = [
            v if isinstance(v, Label) else Label(v) for v in self.right_predicate_labels
        ]

        if self.left_subject_is_functional is not None and not isinstance(
            self.left_subject_is_functional, str
        ):
            self.left_subject_is_functional = str(self.left_subject_is_functional)

        if self.left_object_is_functional is not None and not isinstance(
            self.left_object_is_functional, str
        ):
            self.left_object_is_functional = str(self.left_object_is_functional)

        if self.subject_mapping_predicate is not None and not isinstance(
            self.subject_mapping_predicate, EntityReference
        ):
            self.subject_mapping_predicate = EntityReference(self.subject_mapping_predicate)

        if self.object_mapping_predicate is not None and not isinstance(
            self.object_mapping_predicate, EntityReference
        ):
            self.object_mapping_predicate = EntityReference(self.object_mapping_predicate)

        if not isinstance(self.right_intermediate_ids, list):
            self.right_intermediate_ids = (
                [self.right_intermediate_ids] if self.right_intermediate_ids is not None else []
            )
        self.right_intermediate_ids = [
            v if isinstance(v, EntityReference) else EntityReference(v)
            for v in self.right_intermediate_ids
        ]

        if self.subject_mapping_cardinality is not None and not isinstance(
            self.subject_mapping_cardinality, MappingCardinalityEnum
        ):
            self.subject_mapping_cardinality = MappingCardinalityEnum(
                self.subject_mapping_cardinality
            )

        if self.object_mapping_cardinality is not None and not isinstance(
            self.object_mapping_cardinality, MappingCardinalityEnum
        ):
            self.object_mapping_cardinality = MappingCardinalityEnum(
                self.object_mapping_cardinality
            )

        super().__post_init__(**kwargs)


# Enumerations
class DiffCategory(EnumDefinitionImpl):
    """
    Category of the cross-ontology diff, from the perspective of the left-hand edge
    """

    Identical = PermissibleValue(
        text="Identical",
        description="there is a direct analogous direct asserted edge on the right side with the identical predicate",
    )
    MoreSpecificPredicateOnRight = PermissibleValue(
        text="MoreSpecificPredicateOnRight",
        description="there is an analogous edge on the right side with a more specific but non-identical predicate",
    )
    LessSpecificPredicateOnRight = PermissibleValue(
        text="LessSpecificPredicateOnRight",
        description="there is an analogous edge on the right side with a less specific but non-identical predicate",
    )
    LeftEntailedByRight = PermissibleValue(
        text="LeftEntailedByRight",
        description="there is an analogous edge on the right side, where that edge is different from but entailed by the one on the right",
    )
    RightEntailedByLeft = PermissibleValue(
        text="RightEntailedByLeft",
        description="there is an analogous edge on the right side, where that edge is different from but entails the one on the right",
    )
    IndirectFormOfEdgeOnRight = PermissibleValue(
        text="IndirectFormOfEdgeOnRight",
        description="there is no direct analogous right side edge but an analogous edge can be entailed",
    )
    RightNodesAreIdentical = PermissibleValue(
        text="RightNodesAreIdentical",
        description="a special case where both the left subject and left object map to the same node on the right",
    )
    NonEntailedRelationship = PermissibleValue(
        text="NonEntailedRelationship",
        description="there is an analogous edge on the right side with a different predicate that is neither more specific nor less specific",
    )
    NoRelationship = PermissibleValue(
        text="NoRelationship",
        description="there is no relationship between the right object and right subject",
    )
    MissingMapping = PermissibleValue(
        text="MissingMapping", description="one or both mappings are missing"
    )
    MissingSubjectMapping = PermissibleValue(
        text="MissingSubjectMapping", description="there is no mapping for the subject"
    )
    MissingObjectMapping = PermissibleValue(
        text="MissingObjectMapping", description="there is no mapping for the object"
    )

    _defn = EnumDefinition(
        name="DiffCategory",
        description="Category of the cross-ontology diff, from the perspective of the left-hand edge",
    )


class MappingCardinalityEnum(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="MappingCardinalityEnum",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "1:1", PermissibleValue(text="1:1", description="One-to-one mapping"))
        setattr(cls, "1:n", PermissibleValue(text="1:n", description="One-to-many mapping"))
        setattr(cls, "n:1", PermissibleValue(text="n:1", description="Many-to-one mapping"))
        setattr(cls, "1:0", PermissibleValue(text="1:0", description="One-to-none mapping"))
        setattr(cls, "0:1", PermissibleValue(text="0:1", description="None-to-one mapping"))
        setattr(cls, "n:n", PermissibleValue(text="n:n", description="Many-to-many mapping"))


# Slots
class slots:
    pass


slots.label = Slot(
    uri=RDFS.label,
    name="label",
    curie=RDFS.curie("label"),
    model_uri=ANN.label,
    domain=None,
    range=Optional[str],
)

slots.side = Slot(
    uri=ANN.side,
    name="side",
    curie=ANN.curie("side"),
    model_uri=ANN.side,
    domain=None,
    range=Optional[str],
)

slots.left_side = Slot(
    uri=ANN.left_side,
    name="left_side",
    curie=ANN.curie("left_side"),
    model_uri=ANN.left_side,
    domain=None,
    range=Optional[str],
)

slots.right_side = Slot(
    uri=ANN.right_side,
    name="right_side",
    curie=ANN.curie("right_side"),
    model_uri=ANN.right_side,
    domain=None,
    range=Optional[str],
)

slots.subject = Slot(
    uri=RDF.subject,
    name="subject",
    curie=RDF.curie("subject"),
    model_uri=ANN.subject,
    domain=None,
    range=Optional[str],
)

slots.predicate = Slot(
    uri=RDF.predicate,
    name="predicate",
    curie=RDF.curie("predicate"),
    model_uri=ANN.predicate,
    domain=None,
    range=Optional[str],
)

slots.object = Slot(
    uri=RDF.object,
    name="object",
    curie=RDF.curie("object"),
    model_uri=ANN.object,
    domain=None,
    range=Optional[str],
)

slots.is_functional = Slot(
    uri=ANN.is_functional,
    name="is_functional",
    curie=ANN.curie("is_functional"),
    model_uri=ANN.is_functional,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.structureDiffResultSet__results = Slot(
    uri=ANN.results,
    name="structureDiffResultSet__results",
    curie=ANN.curie("results"),
    model_uri=ANN.structureDiffResultSet__results,
    domain=None,
    range=Optional[Union[Union[dict, RelationalDiff], List[Union[dict, RelationalDiff]]]],
)

slots.structureDiffResultSet__left_source = Slot(
    uri=ANN.left_source,
    name="structureDiffResultSet__left_source",
    curie=ANN.curie("left_source"),
    model_uri=ANN.structureDiffResultSet__left_source,
    domain=None,
    range=Optional[str],
)

slots.structureDiffResultSet__right_source = Slot(
    uri=ANN.right_source,
    name="structureDiffResultSet__right_source",
    curie=ANN.curie("right_source"),
    model_uri=ANN.structureDiffResultSet__right_source,
    domain=None,
    range=Optional[str],
)

slots.relationalDiff__category = Slot(
    uri=ANN.category,
    name="relationalDiff__category",
    curie=ANN.curie("category"),
    model_uri=ANN.relationalDiff__category,
    domain=None,
    range=Optional[Union[str, "DiffCategory"]],
)

slots.relationalDiff__left_subject_id = Slot(
    uri=ANN.left_subject_id,
    name="relationalDiff__left_subject_id",
    curie=ANN.curie("left_subject_id"),
    model_uri=ANN.relationalDiff__left_subject_id,
    domain=None,
    range=Union[str, EntityReference],
)

slots.relationalDiff__left_object_id = Slot(
    uri=ANN.left_object_id,
    name="relationalDiff__left_object_id",
    curie=ANN.curie("left_object_id"),
    model_uri=ANN.relationalDiff__left_object_id,
    domain=None,
    range=Union[str, EntityReference],
)

slots.relationalDiff__left_predicate_id = Slot(
    uri=ANN.left_predicate_id,
    name="relationalDiff__left_predicate_id",
    curie=ANN.curie("left_predicate_id"),
    model_uri=ANN.relationalDiff__left_predicate_id,
    domain=None,
    range=Union[str, EntityReference],
)

slots.relationalDiff__left_subject_label = Slot(
    uri=ANN.left_subject_label,
    name="relationalDiff__left_subject_label",
    curie=ANN.curie("left_subject_label"),
    model_uri=ANN.relationalDiff__left_subject_label,
    domain=None,
    range=Optional[Union[str, Label]],
)

slots.relationalDiff__left_object_label = Slot(
    uri=ANN.left_object_label,
    name="relationalDiff__left_object_label",
    curie=ANN.curie("left_object_label"),
    model_uri=ANN.relationalDiff__left_object_label,
    domain=None,
    range=Optional[Union[str, Label]],
)

slots.relationalDiff__left_predicate_label = Slot(
    uri=ANN.left_predicate_label,
    name="relationalDiff__left_predicate_label",
    curie=ANN.curie("left_predicate_label"),
    model_uri=ANN.relationalDiff__left_predicate_label,
    domain=None,
    range=Optional[Union[str, Label]],
)

slots.relationalDiff__right_subject_id = Slot(
    uri=ANN.right_subject_id,
    name="relationalDiff__right_subject_id",
    curie=ANN.curie("right_subject_id"),
    model_uri=ANN.relationalDiff__right_subject_id,
    domain=None,
    range=Optional[Union[str, EntityReference]],
)

slots.relationalDiff__right_object_id = Slot(
    uri=ANN.right_object_id,
    name="relationalDiff__right_object_id",
    curie=ANN.curie("right_object_id"),
    model_uri=ANN.relationalDiff__right_object_id,
    domain=None,
    range=Optional[Union[str, EntityReference]],
)

slots.relationalDiff__right_predicate_ids = Slot(
    uri=ANN.right_predicate_ids,
    name="relationalDiff__right_predicate_ids",
    curie=ANN.curie("right_predicate_ids"),
    model_uri=ANN.relationalDiff__right_predicate_ids,
    domain=None,
    range=Optional[Union[Union[str, EntityReference], List[Union[str, EntityReference]]]],
)

slots.relationalDiff__right_subject_label = Slot(
    uri=ANN.right_subject_label,
    name="relationalDiff__right_subject_label",
    curie=ANN.curie("right_subject_label"),
    model_uri=ANN.relationalDiff__right_subject_label,
    domain=None,
    range=Optional[Union[str, Label]],
)

slots.relationalDiff__right_object_label = Slot(
    uri=ANN.right_object_label,
    name="relationalDiff__right_object_label",
    curie=ANN.curie("right_object_label"),
    model_uri=ANN.relationalDiff__right_object_label,
    domain=None,
    range=Optional[Union[str, Label]],
)

slots.relationalDiff__right_predicate_labels = Slot(
    uri=ANN.right_predicate_labels,
    name="relationalDiff__right_predicate_labels",
    curie=ANN.curie("right_predicate_labels"),
    model_uri=ANN.relationalDiff__right_predicate_labels,
    domain=None,
    range=Optional[Union[Union[str, Label], List[Union[str, Label]]]],
)

slots.relationalDiff__left_subject_is_functional = Slot(
    uri=ANN.left_subject_is_functional,
    name="relationalDiff__left_subject_is_functional",
    curie=ANN.curie("left_subject_is_functional"),
    model_uri=ANN.relationalDiff__left_subject_is_functional,
    domain=None,
    range=Optional[str],
)

slots.relationalDiff__left_object_is_functional = Slot(
    uri=ANN.left_object_is_functional,
    name="relationalDiff__left_object_is_functional",
    curie=ANN.curie("left_object_is_functional"),
    model_uri=ANN.relationalDiff__left_object_is_functional,
    domain=None,
    range=Optional[str],
)

slots.relationalDiff__subject_mapping_predicate = Slot(
    uri=ANN.subject_mapping_predicate,
    name="relationalDiff__subject_mapping_predicate",
    curie=ANN.curie("subject_mapping_predicate"),
    model_uri=ANN.relationalDiff__subject_mapping_predicate,
    domain=None,
    range=Optional[Union[str, EntityReference]],
)

slots.relationalDiff__object_mapping_predicate = Slot(
    uri=ANN.object_mapping_predicate,
    name="relationalDiff__object_mapping_predicate",
    curie=ANN.curie("object_mapping_predicate"),
    model_uri=ANN.relationalDiff__object_mapping_predicate,
    domain=None,
    range=Optional[Union[str, EntityReference]],
)

slots.relationalDiff__right_intermediate_ids = Slot(
    uri=ANN.right_intermediate_ids,
    name="relationalDiff__right_intermediate_ids",
    curie=ANN.curie("right_intermediate_ids"),
    model_uri=ANN.relationalDiff__right_intermediate_ids,
    domain=None,
    range=Optional[Union[Union[str, EntityReference], List[Union[str, EntityReference]]]],
)

slots.relationalDiff__subject_mapping_cardinality = Slot(
    uri=ANN.subject_mapping_cardinality,
    name="relationalDiff__subject_mapping_cardinality",
    curie=ANN.curie("subject_mapping_cardinality"),
    model_uri=ANN.relationalDiff__subject_mapping_cardinality,
    domain=None,
    range=Optional[Union[str, "MappingCardinalityEnum"]],
)

slots.relationalDiff__object_mapping_cardinality = Slot(
    uri=ANN.object_mapping_cardinality,
    name="relationalDiff__object_mapping_cardinality",
    curie=ANN.curie("object_mapping_cardinality"),
    model_uri=ANN.relationalDiff__object_mapping_cardinality,
    domain=None,
    range=Optional[Union[str, "MappingCardinalityEnum"]],
)
