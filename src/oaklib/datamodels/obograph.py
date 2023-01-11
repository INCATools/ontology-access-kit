# Auto generated from obograph.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-01-11T14:21:08
# Schema: obographs_datamodel
#
# id: https://github.com/geneontology/obographs
# description: Schema for benchmarking based on obographs
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
from linkml_runtime.linkml_model.types import Boolean, String, Uri
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import URI, Bool, bnode, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str,
)
from rdflib import Namespace, URIRef

metamodel_version = "1.7.0"
version = "0.0.1"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
OG = CurieNamespace("og", "https://github.com/geneontology/obographs/")
OIO = CurieNamespace("oio", "http://www.geneontology.org/formats/oboInOwl#")
OWL = CurieNamespace("owl", "http://www.w3.org/2002/07/owl#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SDO = CurieNamespace("sdo", "https://schema.org/")
SH = CurieNamespace("sh", "https://w3id.org/shacl/")
SKOS = CurieNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = OG


# Types

# Class references
class GraphId(extended_str):
    pass


class NodeId(extended_str):
    pass


@dataclass
class GraphDocument(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.GraphDocument
    class_class_curie: ClassVar[str] = "og:GraphDocument"
    class_name: ClassVar[str] = "GraphDocument"
    class_model_uri: ClassVar[URIRef] = OG.GraphDocument

    meta: Optional[Union[dict, "Meta"]] = None
    graphs: Optional[
        Union[Dict[Union[str, GraphId], Union[dict, "Graph"]], List[Union[dict, "Graph"]]]
    ] = empty_dict()
    prefixes: Optional[
        Union[Union[dict, "PrefixDeclaration"], List[Union[dict, "PrefixDeclaration"]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        self._normalize_inlined_as_list(
            slot_name="graphs", slot_type=Graph, key_name="id", keyed=True
        )

        if not isinstance(self.prefixes, list):
            self.prefixes = [self.prefixes] if self.prefixes is not None else []
        self.prefixes = [
            v if isinstance(v, PrefixDeclaration) else PrefixDeclaration(**as_dict(v))
            for v in self.prefixes
        ]

        super().__post_init__(**kwargs)


@dataclass
class PrefixDeclaration(YAMLRoot):
    """
    maps individual prefix to namespace
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH.PrefixDeclaration
    class_class_curie: ClassVar[str] = "sh:PrefixDeclaration"
    class_name: ClassVar[str] = "PrefixDeclaration"
    class_model_uri: ClassVar[URIRef] = OG.PrefixDeclaration

    prefix: Optional[str] = None
    namespace: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.prefix is not None and not isinstance(self.prefix, str):
            self.prefix = str(self.prefix)

        if self.namespace is not None and not isinstance(self.namespace, URI):
            self.namespace = URI(self.namespace)

        super().__post_init__(**kwargs)


@dataclass
class Graph(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Ontology
    class_class_curie: ClassVar[str] = "owl:Ontology"
    class_name: ClassVar[str] = "Graph"
    class_model_uri: ClassVar[URIRef] = OG.Graph

    id: Union[str, GraphId] = None
    lbl: Optional[str] = None
    meta: Optional[Union[dict, "Meta"]] = None
    nodes: Optional[
        Union[Dict[Union[str, NodeId], Union[dict, "Node"]], List[Union[dict, "Node"]]]
    ] = empty_dict()
    edges: Optional[Union[Union[dict, "Edge"], List[Union[dict, "Edge"]]]] = empty_list()
    equivalentNodesSets: Optional[
        Union[Union[dict, "EquivalentNodesSet"], List[Union[dict, "EquivalentNodesSet"]]]
    ] = empty_list()
    logicalDefinitionAxioms: Optional[
        Union[Union[dict, "LogicalDefinitionAxiom"], List[Union[dict, "LogicalDefinitionAxiom"]]]
    ] = empty_list()
    domainRangeAxioms: Optional[
        Union[Union[dict, "DomainRangeAxiom"], List[Union[dict, "DomainRangeAxiom"]]]
    ] = empty_list()
    allValuesFromEdges: Optional[
        Union[Union[dict, "Edge"], List[Union[dict, "Edge"]]]
    ] = empty_list()
    propertyChainAxioms: Optional[
        Union[Union[dict, "PropertyChainAxiom"], List[Union[dict, "PropertyChainAxiom"]]]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GraphId):
            self.id = GraphId(self.id)

        if self.lbl is not None and not isinstance(self.lbl, str):
            self.lbl = str(self.lbl)

        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        self._normalize_inlined_as_list(
            slot_name="nodes", slot_type=Node, key_name="id", keyed=True
        )

        if not isinstance(self.edges, list):
            self.edges = [self.edges] if self.edges is not None else []
        self.edges = [v if isinstance(v, Edge) else Edge(**as_dict(v)) for v in self.edges]

        if not isinstance(self.equivalentNodesSets, list):
            self.equivalentNodesSets = (
                [self.equivalentNodesSets] if self.equivalentNodesSets is not None else []
            )
        self.equivalentNodesSets = [
            v if isinstance(v, EquivalentNodesSet) else EquivalentNodesSet(**as_dict(v))
            for v in self.equivalentNodesSets
        ]

        if not isinstance(self.logicalDefinitionAxioms, list):
            self.logicalDefinitionAxioms = (
                [self.logicalDefinitionAxioms] if self.logicalDefinitionAxioms is not None else []
            )
        self.logicalDefinitionAxioms = [
            v if isinstance(v, LogicalDefinitionAxiom) else LogicalDefinitionAxiom(**as_dict(v))
            for v in self.logicalDefinitionAxioms
        ]

        if not isinstance(self.domainRangeAxioms, list):
            self.domainRangeAxioms = (
                [self.domainRangeAxioms] if self.domainRangeAxioms is not None else []
            )
        self.domainRangeAxioms = [
            v if isinstance(v, DomainRangeAxiom) else DomainRangeAxiom(**as_dict(v))
            for v in self.domainRangeAxioms
        ]

        if not isinstance(self.allValuesFromEdges, list):
            self.allValuesFromEdges = (
                [self.allValuesFromEdges] if self.allValuesFromEdges is not None else []
            )
        self.allValuesFromEdges = [
            v if isinstance(v, Edge) else Edge(**as_dict(v)) for v in self.allValuesFromEdges
        ]

        if not isinstance(self.propertyChainAxioms, list):
            self.propertyChainAxioms = (
                [self.propertyChainAxioms] if self.propertyChainAxioms is not None else []
            )
        self.propertyChainAxioms = [
            v if isinstance(v, PropertyChainAxiom) else PropertyChainAxiom(**as_dict(v))
            for v in self.propertyChainAxioms
        ]

        super().__post_init__(**kwargs)


@dataclass
class Node(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = RDF.Resource
    class_class_curie: ClassVar[str] = "rdf:Resource"
    class_name: ClassVar[str] = "Node"
    class_model_uri: ClassVar[URIRef] = OG.Node

    id: Union[str, NodeId] = None
    lbl: Optional[str] = None
    type: Optional[str] = None
    meta: Optional[Union[dict, "Meta"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NodeId):
            self.id = NodeId(self.id)

        if self.lbl is not None and not isinstance(self.lbl, str):
            self.lbl = str(self.lbl)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        super().__post_init__(**kwargs)


@dataclass
class Edge(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.Edge
    class_class_curie: ClassVar[str] = "og:Edge"
    class_name: ClassVar[str] = "Edge"
    class_model_uri: ClassVar[URIRef] = OG.Edge

    sub: Optional[str] = None
    pred: Optional[str] = None
    obj: Optional[str] = None
    meta: Optional[Union[dict, "Meta"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.sub is not None and not isinstance(self.sub, str):
            self.sub = str(self.sub)

        if self.pred is not None and not isinstance(self.pred, str):
            self.pred = str(self.pred)

        if self.obj is not None and not isinstance(self.obj, str):
            self.obj = str(self.obj)

        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        super().__post_init__(**kwargs)


@dataclass
class Meta(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.Meta
    class_class_curie: ClassVar[str] = "og:Meta"
    class_name: ClassVar[str] = "Meta"
    class_model_uri: ClassVar[URIRef] = OG.Meta

    subsets: Optional[Union[str, List[str]]] = empty_list()
    version: Optional[str] = None
    comments: Optional[Union[str, List[str]]] = empty_list()
    definition: Optional[Union[dict, "DefinitionPropertyValue"]] = None
    xrefs: Optional[
        Union[Union[dict, "XrefPropertyValue"], List[Union[dict, "XrefPropertyValue"]]]
    ] = empty_list()
    synonyms: Optional[
        Union[Union[dict, "SynonymPropertyValue"], List[Union[dict, "SynonymPropertyValue"]]]
    ] = empty_list()
    basicPropertyValues: Optional[
        Union[Union[dict, "BasicPropertyValue"], List[Union[dict, "BasicPropertyValue"]]]
    ] = empty_list()
    deprecated: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.subsets, list):
            self.subsets = [self.subsets] if self.subsets is not None else []
        self.subsets = [v if isinstance(v, str) else str(v) for v in self.subsets]

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if not isinstance(self.comments, list):
            self.comments = [self.comments] if self.comments is not None else []
        self.comments = [v if isinstance(v, str) else str(v) for v in self.comments]

        if self.definition is not None and not isinstance(self.definition, DefinitionPropertyValue):
            self.definition = DefinitionPropertyValue(**as_dict(self.definition))

        if not isinstance(self.xrefs, list):
            self.xrefs = [self.xrefs] if self.xrefs is not None else []
        self.xrefs = [
            v if isinstance(v, XrefPropertyValue) else XrefPropertyValue(**as_dict(v))
            for v in self.xrefs
        ]

        if not isinstance(self.synonyms, list):
            self.synonyms = [self.synonyms] if self.synonyms is not None else []
        self.synonyms = [
            v if isinstance(v, SynonymPropertyValue) else SynonymPropertyValue(**as_dict(v))
            for v in self.synonyms
        ]

        if not isinstance(self.basicPropertyValues, list):
            self.basicPropertyValues = (
                [self.basicPropertyValues] if self.basicPropertyValues is not None else []
            )
        self.basicPropertyValues = [
            v if isinstance(v, BasicPropertyValue) else BasicPropertyValue(**as_dict(v))
            for v in self.basicPropertyValues
        ]

        if self.deprecated is not None and not isinstance(self.deprecated, Bool):
            self.deprecated = Bool(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass
class PropertyValue(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.PropertyValue
    class_class_curie: ClassVar[str] = "og:PropertyValue"
    class_name: ClassVar[str] = "PropertyValue"
    class_model_uri: ClassVar[URIRef] = OG.PropertyValue

    pred: Optional[str] = None
    val: Optional[str] = None
    xrefs: Optional[Union[str, List[str]]] = empty_list()
    meta: Optional[Union[dict, Meta]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.pred is not None and not isinstance(self.pred, str):
            self.pred = str(self.pred)

        if self.val is not None and not isinstance(self.val, str):
            self.val = str(self.val)

        if not isinstance(self.xrefs, list):
            self.xrefs = [self.xrefs] if self.xrefs is not None else []
        self.xrefs = [v if isinstance(v, str) else str(v) for v in self.xrefs]

        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        super().__post_init__(**kwargs)


class DefinitionPropertyValue(PropertyValue):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.DefinitionPropertyValue
    class_class_curie: ClassVar[str] = "og:DefinitionPropertyValue"
    class_name: ClassVar[str] = "DefinitionPropertyValue"
    class_model_uri: ClassVar[URIRef] = OG.DefinitionPropertyValue


class BasicPropertyValue(PropertyValue):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.BasicPropertyValue
    class_class_curie: ClassVar[str] = "og:BasicPropertyValue"
    class_name: ClassVar[str] = "BasicPropertyValue"
    class_model_uri: ClassVar[URIRef] = OG.BasicPropertyValue


class XrefPropertyValue(PropertyValue):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.XrefPropertyValue
    class_class_curie: ClassVar[str] = "og:XrefPropertyValue"
    class_name: ClassVar[str] = "XrefPropertyValue"
    class_model_uri: ClassVar[URIRef] = OG.XrefPropertyValue


@dataclass
class SynonymPropertyValue(PropertyValue):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.SynonymPropertyValue
    class_class_curie: ClassVar[str] = "og:SynonymPropertyValue"
    class_name: ClassVar[str] = "SynonymPropertyValue"
    class_model_uri: ClassVar[URIRef] = OG.SynonymPropertyValue

    synonymType: Optional[str] = None
    isExact: Optional[Union[bool, Bool]] = None
    pred: Optional[Union[str, "ScopeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.synonymType is not None and not isinstance(self.synonymType, str):
            self.synonymType = str(self.synonymType)

        if self.isExact is not None and not isinstance(self.isExact, Bool):
            self.isExact = Bool(self.isExact)

        if self.pred is not None and not isinstance(self.pred, ScopeEnum):
            self.pred = ScopeEnum(self.pred)

        super().__post_init__(**kwargs)


@dataclass
class Axiom(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.Axiom
    class_class_curie: ClassVar[str] = "og:Axiom"
    class_name: ClassVar[str] = "Axiom"
    class_model_uri: ClassVar[URIRef] = OG.Axiom

    meta: Optional[Union[dict, Meta]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        super().__post_init__(**kwargs)


@dataclass
class DomainRangeAxiom(Axiom):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.DomainRangeAxiom
    class_class_curie: ClassVar[str] = "og:DomainRangeAxiom"
    class_name: ClassVar[str] = "DomainRangeAxiom"
    class_model_uri: ClassVar[URIRef] = OG.DomainRangeAxiom

    predicateId: Optional[str] = None
    domainClassIds: Optional[Union[str, List[str]]] = empty_list()
    rangeClassIds: Optional[Union[str, List[str]]] = empty_list()
    allValuesFromEdges: Optional[Union[Union[dict, Edge], List[Union[dict, Edge]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.predicateId is not None and not isinstance(self.predicateId, str):
            self.predicateId = str(self.predicateId)

        if not isinstance(self.domainClassIds, list):
            self.domainClassIds = [self.domainClassIds] if self.domainClassIds is not None else []
        self.domainClassIds = [v if isinstance(v, str) else str(v) for v in self.domainClassIds]

        if not isinstance(self.rangeClassIds, list):
            self.rangeClassIds = [self.rangeClassIds] if self.rangeClassIds is not None else []
        self.rangeClassIds = [v if isinstance(v, str) else str(v) for v in self.rangeClassIds]

        if not isinstance(self.allValuesFromEdges, list):
            self.allValuesFromEdges = (
                [self.allValuesFromEdges] if self.allValuesFromEdges is not None else []
            )
        self.allValuesFromEdges = [
            v if isinstance(v, Edge) else Edge(**as_dict(v)) for v in self.allValuesFromEdges
        ]

        super().__post_init__(**kwargs)


@dataclass
class EquivalentNodesSet(Axiom):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.equivalentClass
    class_class_curie: ClassVar[str] = "owl:equivalentClass"
    class_name: ClassVar[str] = "EquivalentNodesSet"
    class_model_uri: ClassVar[URIRef] = OG.EquivalentNodesSet

    representativeNodeId: Optional[str] = None
    nodeIds: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.representativeNodeId is not None and not isinstance(self.representativeNodeId, str):
            self.representativeNodeId = str(self.representativeNodeId)

        if not isinstance(self.nodeIds, list):
            self.nodeIds = [self.nodeIds] if self.nodeIds is not None else []
        self.nodeIds = [v if isinstance(v, str) else str(v) for v in self.nodeIds]

        super().__post_init__(**kwargs)


@dataclass
class ExistentialRestrictionExpression(YAMLRoot):
    """
    An existential restriction (OWL some values from) expression
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Restriction
    class_class_curie: ClassVar[str] = "owl:Restriction"
    class_name: ClassVar[str] = "ExistentialRestrictionExpression"
    class_model_uri: ClassVar[URIRef] = OG.ExistentialRestrictionExpression

    fillerId: Optional[str] = None
    propertyId: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.fillerId is not None and not isinstance(self.fillerId, str):
            self.fillerId = str(self.fillerId)

        if self.propertyId is not None and not isinstance(self.propertyId, str):
            self.propertyId = str(self.propertyId)

        super().__post_init__(**kwargs)


@dataclass
class LogicalDefinitionAxiom(Axiom):
    """
    An axiom that defines a class in terms of a genus or set of genus classes and a set of differentia
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.LogicalDefinitionAxiom
    class_class_curie: ClassVar[str] = "og:LogicalDefinitionAxiom"
    class_name: ClassVar[str] = "LogicalDefinitionAxiom"
    class_model_uri: ClassVar[URIRef] = OG.LogicalDefinitionAxiom

    definedClassId: str = None
    genusIds: Optional[Union[str, List[str]]] = empty_list()
    restrictions: Optional[
        Union[
            Union[dict, ExistentialRestrictionExpression],
            List[Union[dict, ExistentialRestrictionExpression]],
        ]
    ] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.definedClassId):
            self.MissingRequiredField("definedClassId")
        if not isinstance(self.definedClassId, str):
            self.definedClassId = str(self.definedClassId)

        if not isinstance(self.genusIds, list):
            self.genusIds = [self.genusIds] if self.genusIds is not None else []
        self.genusIds = [v if isinstance(v, str) else str(v) for v in self.genusIds]

        if not isinstance(self.restrictions, list):
            self.restrictions = [self.restrictions] if self.restrictions is not None else []
        self.restrictions = [
            v
            if isinstance(v, ExistentialRestrictionExpression)
            else ExistentialRestrictionExpression(**as_dict(v))
            for v in self.restrictions
        ]

        super().__post_init__(**kwargs)


@dataclass
class PropertyChainAxiom(Axiom):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OG.PropertyChainAxiom
    class_class_curie: ClassVar[str] = "og:PropertyChainAxiom"
    class_name: ClassVar[str] = "PropertyChainAxiom"
    class_model_uri: ClassVar[URIRef] = OG.PropertyChainAxiom

    predicateId: Optional[str] = None
    chainPredicateIds: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.predicateId is not None and not isinstance(self.predicateId, str):
            self.predicateId = str(self.predicateId)

        if not isinstance(self.chainPredicateIds, list):
            self.chainPredicateIds = (
                [self.chainPredicateIds] if self.chainPredicateIds is not None else []
            )
        self.chainPredicateIds = [
            v if isinstance(v, str) else str(v) for v in self.chainPredicateIds
        ]

        super().__post_init__(**kwargs)


# Enumerations
class ScopeEnum(EnumDefinitionImpl):

    hasExactSynonym = PermissibleValue(text="hasExactSynonym", meaning=OIO.hasExactSynonym)
    hasNarrowSynonym = PermissibleValue(text="hasNarrowSynonym", meaning=OIO.hasNarrowSynonym)
    hasBroadSynonym = PermissibleValue(text="hasBroadSynonym", meaning=OIO.hasBroadSynonym)
    hasRelatedSynonym = PermissibleValue(text="hasRelatedSynonym", meaning=OIO.hasRelatedSynonym)

    _defn = EnumDefinition(
        name="ScopeEnum",
    )


# Slots
class slots:
    pass


slots.id = Slot(
    uri=OG.id, name="id", curie=OG.curie("id"), model_uri=OG.id, domain=None, range=URIRef
)

slots.sub = Slot(
    uri=OG.sub,
    name="sub",
    curie=OG.curie("sub"),
    model_uri=OG.sub,
    domain=None,
    range=Optional[str],
)

slots.pred = Slot(
    uri=OG.pred,
    name="pred",
    curie=OG.curie("pred"),
    model_uri=OG.pred,
    domain=None,
    range=Optional[str],
)

slots.obj = Slot(
    uri=OG.obj,
    name="obj",
    curie=OG.curie("obj"),
    model_uri=OG.obj,
    domain=None,
    range=Optional[str],
)

slots.val = Slot(
    uri=OG.val,
    name="val",
    curie=OG.curie("val"),
    model_uri=OG.val,
    domain=None,
    range=Optional[str],
)

slots.lbl = Slot(
    uri=OG.lbl,
    name="lbl",
    curie=OG.curie("lbl"),
    model_uri=OG.lbl,
    domain=None,
    range=Optional[str],
)

slots.type = Slot(
    uri=OG.type,
    name="type",
    curie=OG.curie("type"),
    model_uri=OG.type,
    domain=None,
    range=Optional[str],
)

slots.meta = Slot(
    uri=OG.meta,
    name="meta",
    curie=OG.curie("meta"),
    model_uri=OG.meta,
    domain=None,
    range=Optional[Union[dict, Meta]],
)

slots.definition = Slot(
    uri=OG.definition,
    name="definition",
    curie=OG.curie("definition"),
    model_uri=OG.definition,
    domain=None,
    range=Optional[Union[dict, DefinitionPropertyValue]],
)

slots.basicPropertyValues = Slot(
    uri=OG.basicPropertyValues,
    name="basicPropertyValues",
    curie=OG.curie("basicPropertyValues"),
    model_uri=OG.basicPropertyValues,
    domain=None,
    range=Optional[Union[Union[dict, BasicPropertyValue], List[Union[dict, BasicPropertyValue]]]],
)

slots.comments = Slot(
    uri=OG.comments,
    name="comments",
    curie=OG.curie("comments"),
    model_uri=OG.comments,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.version = Slot(
    uri=OG.version,
    name="version",
    curie=OG.curie("version"),
    model_uri=OG.version,
    domain=None,
    range=Optional[str],
)

slots.deprecated = Slot(
    uri=OG.deprecated,
    name="deprecated",
    curie=OG.curie("deprecated"),
    model_uri=OG.deprecated,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.subsets = Slot(
    uri=OG.subsets,
    name="subsets",
    curie=OG.curie("subsets"),
    model_uri=OG.subsets,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.xrefs = Slot(
    uri=OG.xrefs,
    name="xrefs",
    curie=OG.curie("xrefs"),
    model_uri=OG.xrefs,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.nodes = Slot(
    uri=OG.nodes,
    name="nodes",
    curie=OG.curie("nodes"),
    model_uri=OG.nodes,
    domain=None,
    range=Optional[Union[Dict[Union[str, NodeId], Union[dict, Node]], List[Union[dict, Node]]]],
)

slots.edges = Slot(
    uri=OG.edges,
    name="edges",
    curie=OG.curie("edges"),
    model_uri=OG.edges,
    domain=None,
    range=Optional[Union[Union[dict, Edge], List[Union[dict, Edge]]]],
)

slots.equivalentNodesSets = Slot(
    uri=OG.equivalentNodesSets,
    name="equivalentNodesSets",
    curie=OG.curie("equivalentNodesSets"),
    model_uri=OG.equivalentNodesSets,
    domain=None,
    range=Optional[Union[Union[dict, EquivalentNodesSet], List[Union[dict, EquivalentNodesSet]]]],
)

slots.logicalDefinitionAxioms = Slot(
    uri=OG.logicalDefinitionAxioms,
    name="logicalDefinitionAxioms",
    curie=OG.curie("logicalDefinitionAxioms"),
    model_uri=OG.logicalDefinitionAxioms,
    domain=None,
    range=Optional[
        Union[Union[dict, LogicalDefinitionAxiom], List[Union[dict, LogicalDefinitionAxiom]]]
    ],
)

slots.domainRangeAxioms = Slot(
    uri=OG.domainRangeAxioms,
    name="domainRangeAxioms",
    curie=OG.curie("domainRangeAxioms"),
    model_uri=OG.domainRangeAxioms,
    domain=None,
    range=Optional[Union[Union[dict, DomainRangeAxiom], List[Union[dict, DomainRangeAxiom]]]],
)

slots.allValuesFromEdges = Slot(
    uri=OG.allValuesFromEdges,
    name="allValuesFromEdges",
    curie=OG.curie("allValuesFromEdges"),
    model_uri=OG.allValuesFromEdges,
    domain=None,
    range=Optional[Union[Union[dict, Edge], List[Union[dict, Edge]]]],
)

slots.propertyChainAxioms = Slot(
    uri=OG.propertyChainAxioms,
    name="propertyChainAxioms",
    curie=OG.curie("propertyChainAxioms"),
    model_uri=OG.propertyChainAxioms,
    domain=None,
    range=Optional[Union[Union[dict, PropertyChainAxiom], List[Union[dict, PropertyChainAxiom]]]],
)

slots.representativeNodeId = Slot(
    uri=OG.representativeNodeId,
    name="representativeNodeId",
    curie=OG.curie("representativeNodeId"),
    model_uri=OG.representativeNodeId,
    domain=None,
    range=Optional[str],
)

slots.chainPredicateIds = Slot(
    uri=OG.chainPredicateIds,
    name="chainPredicateIds",
    curie=OG.curie("chainPredicateIds"),
    model_uri=OG.chainPredicateIds,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.nodeIds = Slot(
    uri=OG.nodeIds,
    name="nodeIds",
    curie=OG.curie("nodeIds"),
    model_uri=OG.nodeIds,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.fillerId = Slot(
    uri=OG.fillerId,
    name="fillerId",
    curie=OG.curie("fillerId"),
    model_uri=OG.fillerId,
    domain=None,
    range=Optional[str],
)

slots.propertyId = Slot(
    uri=OG.propertyId,
    name="propertyId",
    curie=OG.curie("propertyId"),
    model_uri=OG.propertyId,
    domain=None,
    range=Optional[str],
)

slots.predicateId = Slot(
    uri=OG.predicateId,
    name="predicateId",
    curie=OG.curie("predicateId"),
    model_uri=OG.predicateId,
    domain=None,
    range=Optional[str],
)

slots.domainClassIds = Slot(
    uri=OG.domainClassIds,
    name="domainClassIds",
    curie=OG.curie("domainClassIds"),
    model_uri=OG.domainClassIds,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.rangeClassIds = Slot(
    uri=OG.rangeClassIds,
    name="rangeClassIds",
    curie=OG.curie("rangeClassIds"),
    model_uri=OG.rangeClassIds,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.synonyms = Slot(
    uri=OG.synonyms,
    name="synonyms",
    curie=OG.curie("synonyms"),
    model_uri=OG.synonyms,
    domain=None,
    range=Optional[
        Union[Union[dict, SynonymPropertyValue], List[Union[dict, SynonymPropertyValue]]]
    ],
)

slots.synonymType = Slot(
    uri=OG.synonymType,
    name="synonymType",
    curie=OG.curie("synonymType"),
    model_uri=OG.synonymType,
    domain=None,
    range=Optional[str],
)

slots.isExact = Slot(
    uri=OG.isExact,
    name="isExact",
    curie=OG.curie("isExact"),
    model_uri=OG.isExact,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.graphs = Slot(
    uri=OG.graphs,
    name="graphs",
    curie=OG.curie("graphs"),
    model_uri=OG.graphs,
    domain=None,
    range=Optional[Union[Dict[Union[str, GraphId], Union[dict, Graph]], List[Union[dict, Graph]]]],
)

slots.prefixes = Slot(
    uri=SH.declare,
    name="prefixes",
    curie=SH.curie("declare"),
    model_uri=OG.prefixes,
    domain=None,
    range=Optional[Union[Union[dict, PrefixDeclaration], List[Union[dict, PrefixDeclaration]]]],
)

slots.prefixDeclaration__prefix = Slot(
    uri=SH.prefix,
    name="prefixDeclaration__prefix",
    curie=SH.curie("prefix"),
    model_uri=OG.prefixDeclaration__prefix,
    domain=None,
    range=Optional[str],
)

slots.prefixDeclaration__namespace = Slot(
    uri=SH.namespace,
    name="prefixDeclaration__namespace",
    curie=SH.curie("namespace"),
    model_uri=OG.prefixDeclaration__namespace,
    domain=None,
    range=Optional[Union[str, URI]],
)

slots.logicalDefinitionAxiom__definedClassId = Slot(
    uri=OG.definedClassId,
    name="logicalDefinitionAxiom__definedClassId",
    curie=OG.curie("definedClassId"),
    model_uri=OG.logicalDefinitionAxiom__definedClassId,
    domain=None,
    range=str,
)

slots.logicalDefinitionAxiom__genusIds = Slot(
    uri=OG.genusIds,
    name="logicalDefinitionAxiom__genusIds",
    curie=OG.curie("genusIds"),
    model_uri=OG.logicalDefinitionAxiom__genusIds,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.logicalDefinitionAxiom__restrictions = Slot(
    uri=OWL.someValuesFrom,
    name="logicalDefinitionAxiom__restrictions",
    curie=OWL.curie("someValuesFrom"),
    model_uri=OG.logicalDefinitionAxiom__restrictions,
    domain=None,
    range=Optional[
        Union[
            Union[dict, ExistentialRestrictionExpression],
            List[Union[dict, ExistentialRestrictionExpression]],
        ]
    ],
)

slots.Meta_xrefs = Slot(
    uri=OG.xrefs,
    name="Meta_xrefs",
    curie=OG.curie("xrefs"),
    model_uri=OG.Meta_xrefs,
    domain=Meta,
    range=Optional[Union[Union[dict, "XrefPropertyValue"], List[Union[dict, "XrefPropertyValue"]]]],
)

slots.SynonymPropertyValue_pred = Slot(
    uri=OG.pred,
    name="SynonymPropertyValue_pred",
    curie=OG.curie("pred"),
    model_uri=OG.SynonymPropertyValue_pred,
    domain=SynonymPropertyValue,
    range=Optional[Union[str, "ScopeEnum"]],
)
