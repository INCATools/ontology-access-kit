# Auto generated from obograph.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-02-05T11:24:54
# Schema: obographs_datamodel
#
# id: https://github.com/geneontology/obographs
# description: A data model for graph-oriented representations of ontologies. Each ontology is represented as a Graph, and multiple ontologies can be connected together in a GraphDocument.
#   The principle elements of a Graph are Node objects and Edge objects. A Node represents an arbitrary ontology element, including but not limited to the core terms in the ontology. Edges represent simple relationships between Nodes. Nodes and Edges can both have Meta objects attached, providing additional metedata.
#   Not everything in an ontology can be represented as nodes and edges. More complex axioms have specialized structures such as DomainRangeAxiom objects and LogicalDefinitionAxiom.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, String, Uri
from linkml_runtime.utils.metamodelcore import Bool, URI

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OBOGRAPHS = CurieNamespace('obographs', 'https://github.com/geneontology/obographs/')
OIO = CurieNamespace('oio', 'http://www.geneontology.org/formats/oboInOwl#')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SDO = CurieNamespace('sdo', 'https://schema.org/')
SH = CurieNamespace('sh', 'https://w3id.org/shacl/')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = OBOGRAPHS


# Types
class XrefString(String):
    """ A string that is a cross reference to another entity represented in another ontology, vocabulary, database, or website. The string SHOULD be a CURIE or a URL, but this standard relaxes this to a string to support parsing of legacy ontologies that may use other syntaxes. If a CURIE is provided, this SHOULD be registered in a standard registry such as bioregistry. """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "XrefString"
    type_model_uri = OBOGRAPHS.XrefString


class OboIdentifierString(String):
    """ A string that represents an OBO identifier. This MUST be EITHER a PrefixedID (CURIE), an UnprefixedID, or a URI. If the identifier is for a Class, then the identifier MUST be a PrefixedID """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "OboIdentifierString"
    type_model_uri = OBOGRAPHS.OboIdentifierString


class SynonymTypeIdentifierString(String):
    """ A string that represents a synonym type. Note synonym types are distinct from synonym scopes. A synonym type is commonly represented as a plain string such as ABBREVIATION """
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "SynonymTypeIdentifierString"
    type_model_uri = OBOGRAPHS.SynonymTypeIdentifierString


# Class references
class PrefixDeclarationPrefix(extended_str):
    pass


class GraphId(OboIdentifierString):
    pass


class NodeId(OboIdentifierString):
    pass


class SubsetDefinitionId(OboIdentifierString):
    pass


class SynonymTypeDefinitionId(OboIdentifierString):
    pass


@dataclass(repr=False)
class GraphDocument(YAMLRoot):
    """
    A graph document is a collection of graphs together with a set of prefixes that apply across all of them
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["GraphDocument"]
    class_class_curie: ClassVar[str] = "obographs:GraphDocument"
    class_name: ClassVar[str] = "GraphDocument"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.GraphDocument

    meta: Optional[Union[dict, "Meta"]] = None
    graphs: Optional[Union[Dict[Union[str, GraphId], Union[dict, "Graph"]], List[Union[dict, "Graph"]]]] = empty_dict()
    prefixes: Optional[Union[Dict[Union[str, PrefixDeclarationPrefix], Union[dict, "PrefixDeclaration"]], List[Union[dict, "PrefixDeclaration"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        self._normalize_inlined_as_list(slot_name="graphs", slot_type=Graph, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="prefixes", slot_type=PrefixDeclaration, key_name="prefix", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PrefixDeclaration(YAMLRoot):
    """
    A mapping between an individual prefix (e.g. GO) and a namespace (e.g. http://purl.obolibrary.org/obo/GO_)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SH["PrefixDeclaration"]
    class_class_curie: ClassVar[str] = "sh:PrefixDeclaration"
    class_name: ClassVar[str] = "PrefixDeclaration"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.PrefixDeclaration

    prefix: Union[str, PrefixDeclarationPrefix] = None
    namespace: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.prefix):
            self.MissingRequiredField("prefix")
        if not isinstance(self.prefix, PrefixDeclarationPrefix):
            self.prefix = PrefixDeclarationPrefix(self.prefix)

        if self.namespace is not None and not isinstance(self.namespace, URI):
            self.namespace = URI(self.namespace)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Graph(YAMLRoot):
    """
    A graph is a collection of nodes and edges and other axioms that represents a single ontology.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL["Ontology"]
    class_class_curie: ClassVar[str] = "owl:Ontology"
    class_name: ClassVar[str] = "Graph"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.Graph

    id: Union[str, GraphId] = None
    lbl: Optional[str] = None
    prefixes: Optional[Union[Dict[Union[str, PrefixDeclarationPrefix], Union[dict, PrefixDeclaration]], List[Union[dict, PrefixDeclaration]]]] = empty_dict()
    subsetDefinitions: Optional[Union[Dict[Union[str, SubsetDefinitionId], Union[dict, "SubsetDefinition"]], List[Union[dict, "SubsetDefinition"]]]] = empty_dict()
    synonymTypeDefinitions: Optional[Union[Dict[Union[str, SynonymTypeDefinitionId], Union[dict, "SynonymTypeDefinition"]], List[Union[dict, "SynonymTypeDefinition"]]]] = empty_dict()
    meta: Optional[Union[dict, "Meta"]] = None
    nodes: Optional[Union[Dict[Union[str, NodeId], Union[dict, "Node"]], List[Union[dict, "Node"]]]] = empty_dict()
    edges: Optional[Union[Union[dict, "Edge"], List[Union[dict, "Edge"]]]] = empty_list()
    equivalentNodesSets: Optional[Union[Union[dict, "EquivalentNodesSet"], List[Union[dict, "EquivalentNodesSet"]]]] = empty_list()
    logicalDefinitionAxioms: Optional[Union[Union[dict, "LogicalDefinitionAxiom"], List[Union[dict, "LogicalDefinitionAxiom"]]]] = empty_list()
    domainRangeAxioms: Optional[Union[Union[dict, "DomainRangeAxiom"], List[Union[dict, "DomainRangeAxiom"]]]] = empty_list()
    allValuesFromEdges: Optional[Union[Union[dict, "Edge"], List[Union[dict, "Edge"]]]] = empty_list()
    propertyChainAxioms: Optional[Union[Union[dict, "PropertyChainAxiom"], List[Union[dict, "PropertyChainAxiom"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GraphId):
            self.id = GraphId(self.id)

        if self.lbl is not None and not isinstance(self.lbl, str):
            self.lbl = str(self.lbl)

        self._normalize_inlined_as_dict(slot_name="prefixes", slot_type=PrefixDeclaration, key_name="prefix", keyed=True)

        self._normalize_inlined_as_dict(slot_name="subsetDefinitions", slot_type=SubsetDefinition, key_name="id", keyed=True)

        self._normalize_inlined_as_dict(slot_name="synonymTypeDefinitions", slot_type=SynonymTypeDefinition, key_name="id", keyed=True)

        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        self._normalize_inlined_as_list(slot_name="nodes", slot_type=Node, key_name="id", keyed=True)

        if not isinstance(self.edges, list):
            self.edges = [self.edges] if self.edges is not None else []
        self.edges = [v if isinstance(v, Edge) else Edge(**as_dict(v)) for v in self.edges]

        if not isinstance(self.equivalentNodesSets, list):
            self.equivalentNodesSets = [self.equivalentNodesSets] if self.equivalentNodesSets is not None else []
        self.equivalentNodesSets = [v if isinstance(v, EquivalentNodesSet) else EquivalentNodesSet(**as_dict(v)) for v in self.equivalentNodesSets]

        if not isinstance(self.logicalDefinitionAxioms, list):
            self.logicalDefinitionAxioms = [self.logicalDefinitionAxioms] if self.logicalDefinitionAxioms is not None else []
        self.logicalDefinitionAxioms = [v if isinstance(v, LogicalDefinitionAxiom) else LogicalDefinitionAxiom(**as_dict(v)) for v in self.logicalDefinitionAxioms]

        if not isinstance(self.domainRangeAxioms, list):
            self.domainRangeAxioms = [self.domainRangeAxioms] if self.domainRangeAxioms is not None else []
        self.domainRangeAxioms = [v if isinstance(v, DomainRangeAxiom) else DomainRangeAxiom(**as_dict(v)) for v in self.domainRangeAxioms]

        self._normalize_inlined_as_dict(slot_name="allValuesFromEdges", slot_type=Edge, key_name="sub", keyed=False)

        if not isinstance(self.propertyChainAxioms, list):
            self.propertyChainAxioms = [self.propertyChainAxioms] if self.propertyChainAxioms is not None else []
        self.propertyChainAxioms = [v if isinstance(v, PropertyChainAxiom) else PropertyChainAxiom(**as_dict(v)) for v in self.propertyChainAxioms]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Node(YAMLRoot):
    """
    A node is a class, property, or other entity in an ontology
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = RDF["Resource"]
    class_class_curie: ClassVar[str] = "rdf:Resource"
    class_name: ClassVar[str] = "Node"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.Node

    id: Union[str, NodeId] = None
    lbl: Optional[str] = None
    type: Optional[str] = None
    propertyType: Optional[Union[str, "PropertyTypeEnum"]] = None
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

        if self.propertyType is not None and not isinstance(self.propertyType, PropertyTypeEnum):
            self.propertyType = PropertyTypeEnum(self.propertyType)

        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Edge(YAMLRoot):
    """
    An edge is a simple typed relationship between two nodes. When mapping to OWL, an edge represents either (a) s
    SubClassOf o (b) s SubClassOf p some o (c) s p o (where s and o are individuals) (d) s SubPropertyOf o (e) s
    EquivalentTo o (f) s type o
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["Edge"]
    class_class_curie: ClassVar[str] = "obographs:Edge"
    class_name: ClassVar[str] = "Edge"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.Edge

    sub: str = None
    pred: str = None
    obj: str = None
    meta: Optional[Union[dict, "Meta"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.sub):
            self.MissingRequiredField("sub")
        if not isinstance(self.sub, str):
            self.sub = str(self.sub)

        if self._is_empty(self.pred):
            self.MissingRequiredField("pred")
        if not isinstance(self.pred, str):
            self.pred = str(self.pred)

        if self._is_empty(self.obj):
            self.MissingRequiredField("obj")
        if not isinstance(self.obj, str):
            self.obj = str(self.obj)

        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Meta(YAMLRoot):
    """
    A collection of annotations on an entity or ontology or edge or axiom. Metadata typically does not affect the
    logical interpretation of the container but provides useful information to humans or machines.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["Meta"]
    class_class_curie: ClassVar[str] = "obographs:Meta"
    class_name: ClassVar[str] = "Meta"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.Meta

    subsets: Optional[Union[str, List[str]]] = empty_list()
    version: Optional[str] = None
    comments: Optional[Union[str, List[str]]] = empty_list()
    definition: Optional[Union[dict, "DefinitionPropertyValue"]] = None
    xrefs: Optional[Union[Union[dict, "XrefPropertyValue"], List[Union[dict, "XrefPropertyValue"]]]] = empty_list()
    synonyms: Optional[Union[Union[dict, "SynonymPropertyValue"], List[Union[dict, "SynonymPropertyValue"]]]] = empty_list()
    basicPropertyValues: Optional[Union[Union[dict, "BasicPropertyValue"], List[Union[dict, "BasicPropertyValue"]]]] = empty_list()
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
        self.xrefs = [v if isinstance(v, XrefPropertyValue) else XrefPropertyValue(**as_dict(v)) for v in self.xrefs]

        if not isinstance(self.synonyms, list):
            self.synonyms = [self.synonyms] if self.synonyms is not None else []
        self.synonyms = [v if isinstance(v, SynonymPropertyValue) else SynonymPropertyValue(**as_dict(v)) for v in self.synonyms]

        if not isinstance(self.basicPropertyValues, list):
            self.basicPropertyValues = [self.basicPropertyValues] if self.basicPropertyValues is not None else []
        self.basicPropertyValues = [v if isinstance(v, BasicPropertyValue) else BasicPropertyValue(**as_dict(v)) for v in self.basicPropertyValues]

        if self.deprecated is not None and not isinstance(self.deprecated, Bool):
            self.deprecated = Bool(self.deprecated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PropertyValue(YAMLRoot):
    """
    A generic grouping for the different kinds of key-value associations on object. Minimally, a property value has a
    predicate and a value. It can also have a list of xrefs indicating provenance, as well as a metadata object.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["PropertyValue"]
    class_class_curie: ClassVar[str] = "obographs:PropertyValue"
    class_name: ClassVar[str] = "PropertyValue"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.PropertyValue

    pred: Optional[str] = None
    val: Optional[str] = None
    xrefs: Optional[Union[Union[str, XrefString], List[Union[str, XrefString]]]] = empty_list()
    meta: Optional[Union[dict, Meta]] = None
    valType: Optional[str] = None
    lang: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.pred is not None and not isinstance(self.pred, str):
            self.pred = str(self.pred)

        if self.val is not None and not isinstance(self.val, str):
            self.val = str(self.val)

        if not isinstance(self.xrefs, list):
            self.xrefs = [self.xrefs] if self.xrefs is not None else []
        self.xrefs = [v if isinstance(v, XrefString) else XrefString(v) for v in self.xrefs]

        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        if self.valType is not None and not isinstance(self.valType, str):
            self.valType = str(self.valType)

        if self.lang is not None and not isinstance(self.lang, str):
            self.lang = str(self.lang)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DefinitionPropertyValue(PropertyValue):
    """
    A property value that represents an assertion about the textual definition of an entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["DefinitionPropertyValue"]
    class_class_curie: ClassVar[str] = "obographs:DefinitionPropertyValue"
    class_name: ClassVar[str] = "DefinitionPropertyValue"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.DefinitionPropertyValue

    val: Optional[str] = None
    xrefs: Optional[Union[Union[str, XrefString], List[Union[str, XrefString]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.val is not None and not isinstance(self.val, str):
            self.val = str(self.val)

        if not isinstance(self.xrefs, list):
            self.xrefs = [self.xrefs] if self.xrefs is not None else []
        self.xrefs = [v if isinstance(v, XrefString) else XrefString(v) for v in self.xrefs]

        super().__post_init__(**kwargs)


class BasicPropertyValue(PropertyValue):
    """
    A property value that represents an assertion about an entity that is not a definition, synonym, or xref
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["BasicPropertyValue"]
    class_class_curie: ClassVar[str] = "obographs:BasicPropertyValue"
    class_name: ClassVar[str] = "BasicPropertyValue"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.BasicPropertyValue


@dataclass(repr=False)
class XrefPropertyValue(PropertyValue):
    """
    A property value that represents an assertion about an external reference to an entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["XrefPropertyValue"]
    class_class_curie: ClassVar[str] = "obographs:XrefPropertyValue"
    class_name: ClassVar[str] = "XrefPropertyValue"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.XrefPropertyValue

    val: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.val is not None and not isinstance(self.val, str):
            self.val = str(self.val)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SynonymPropertyValue(PropertyValue):
    """
    A property value that represents an assertion about a synonym of an entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["SynonymPropertyValue"]
    class_class_curie: ClassVar[str] = "obographs:SynonymPropertyValue"
    class_name: ClassVar[str] = "SynonymPropertyValue"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.SynonymPropertyValue

    synonymType: Optional[Union[str, SynonymTypeIdentifierString]] = None
    isExact: Optional[Union[bool, Bool]] = None
    pred: Optional[Union[str, "ScopeEnum"]] = None
    val: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.synonymType is not None and not isinstance(self.synonymType, SynonymTypeIdentifierString):
            self.synonymType = SynonymTypeIdentifierString(self.synonymType)

        if self.isExact is not None and not isinstance(self.isExact, Bool):
            self.isExact = Bool(self.isExact)

        if self.pred is not None and not isinstance(self.pred, ScopeEnum):
            self.pred = ScopeEnum(self.pred)

        if self.val is not None and not isinstance(self.val, str):
            self.val = str(self.val)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SubsetDefinition(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OIO["SubsetProperty"]
    class_class_curie: ClassVar[str] = "oio:SubsetProperty"
    class_name: ClassVar[str] = "SubsetDefinition"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.SubsetDefinition

    id: Union[str, SubsetDefinitionId] = None
    lbl: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SubsetDefinitionId):
            self.id = SubsetDefinitionId(self.id)

        if self.lbl is not None and not isinstance(self.lbl, str):
            self.lbl = str(self.lbl)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SynonymTypeDefinition(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OIO["SynonymType"]
    class_class_curie: ClassVar[str] = "oio:SynonymType"
    class_name: ClassVar[str] = "SynonymTypeDefinition"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.SynonymTypeDefinition

    id: Union[str, SynonymTypeDefinitionId] = None
    lbl: Optional[str] = None
    pred: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SynonymTypeDefinitionId):
            self.id = SynonymTypeDefinitionId(self.id)

        if self.lbl is not None and not isinstance(self.lbl, str):
            self.lbl = str(self.lbl)

        if self.pred is not None and not isinstance(self.pred, str):
            self.pred = str(self.pred)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Axiom(YAMLRoot):
    """
    A generic grouping for any OWL axiom or group of axioms that is not captured by existing constructs in this
    standard.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL["Axiom"]
    class_class_curie: ClassVar[str] = "owl:Axiom"
    class_name: ClassVar[str] = "Axiom"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.Axiom

    meta: Optional[Union[dict, Meta]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.meta is not None and not isinstance(self.meta, Meta):
            self.meta = Meta(**as_dict(self.meta))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DomainRangeAxiom(Axiom):
    """
    This groups potentially multiple axioms that constrain the usage of a property depending on some combination of
    domain and range.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["DomainRangeAxiom"]
    class_class_curie: ClassVar[str] = "obographs:DomainRangeAxiom"
    class_name: ClassVar[str] = "DomainRangeAxiom"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.DomainRangeAxiom

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

        self._normalize_inlined_as_dict(slot_name="allValuesFromEdges", slot_type=Edge, key_name="sub", keyed=False)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EquivalentNodesSet(Axiom):
    """
    A clique of nodes that are all mutually equivalent
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL["equivalentClass"]
    class_class_curie: ClassVar[str] = "owl:equivalentClass"
    class_name: ClassVar[str] = "EquivalentNodesSet"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.EquivalentNodesSet

    representativeNodeId: Optional[str] = None
    nodeIds: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.representativeNodeId is not None and not isinstance(self.representativeNodeId, str):
            self.representativeNodeId = str(self.representativeNodeId)

        if not isinstance(self.nodeIds, list):
            self.nodeIds = [self.nodeIds] if self.nodeIds is not None else []
        self.nodeIds = [v if isinstance(v, str) else str(v) for v in self.nodeIds]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExistentialRestrictionExpression(YAMLRoot):
    """
    An existential restriction (OWL some values from) expression
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL["Restriction"]
    class_class_curie: ClassVar[str] = "owl:Restriction"
    class_name: ClassVar[str] = "ExistentialRestrictionExpression"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.ExistentialRestrictionExpression

    fillerId: Optional[str] = None
    propertyId: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.fillerId is not None and not isinstance(self.fillerId, str):
            self.fillerId = str(self.fillerId)

        if self.propertyId is not None and not isinstance(self.propertyId, str):
            self.propertyId = str(self.propertyId)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LogicalDefinitionAxiom(Axiom):
    """
    An axiom that defines a class in terms of a genus or set of genus classes and a set of differentia
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["LogicalDefinitionAxiom"]
    class_class_curie: ClassVar[str] = "obographs:LogicalDefinitionAxiom"
    class_name: ClassVar[str] = "LogicalDefinitionAxiom"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.LogicalDefinitionAxiom

    definedClassId: Union[str, OboIdentifierString] = None
    genusIds: Optional[Union[Union[str, OboIdentifierString], List[Union[str, OboIdentifierString]]]] = empty_list()
    restrictions: Optional[Union[Union[dict, ExistentialRestrictionExpression], List[Union[dict, ExistentialRestrictionExpression]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.definedClassId):
            self.MissingRequiredField("definedClassId")
        if not isinstance(self.definedClassId, OboIdentifierString):
            self.definedClassId = OboIdentifierString(self.definedClassId)

        if not isinstance(self.genusIds, list):
            self.genusIds = [self.genusIds] if self.genusIds is not None else []
        self.genusIds = [v if isinstance(v, OboIdentifierString) else OboIdentifierString(v) for v in self.genusIds]

        if not isinstance(self.restrictions, list):
            self.restrictions = [self.restrictions] if self.restrictions is not None else []
        self.restrictions = [v if isinstance(v, ExistentialRestrictionExpression) else ExistentialRestrictionExpression(**as_dict(v)) for v in self.restrictions]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DisjointClassExpressionsAxiom(Axiom):
    """
    An axiom that defines a set of classes or class expressions as being mutually disjoint. Formally, there exists no
    instance that instantiates more that one of the union of classIds and classExpressions.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["DisjointClassExpressionsAxiom"]
    class_class_curie: ClassVar[str] = "obographs:DisjointClassExpressionsAxiom"
    class_name: ClassVar[str] = "DisjointClassExpressionsAxiom"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.DisjointClassExpressionsAxiom

    classIds: Optional[Union[Union[str, OboIdentifierString], List[Union[str, OboIdentifierString]]]] = empty_list()
    classExpressions: Optional[Union[Union[dict, ExistentialRestrictionExpression], List[Union[dict, ExistentialRestrictionExpression]]]] = empty_list()
    unionEquivalentTo: Optional[Union[str, OboIdentifierString]] = None
    unionEquivalentToExpression: Optional[Union[dict, ExistentialRestrictionExpression]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.classIds, list):
            self.classIds = [self.classIds] if self.classIds is not None else []
        self.classIds = [v if isinstance(v, OboIdentifierString) else OboIdentifierString(v) for v in self.classIds]

        if not isinstance(self.classExpressions, list):
            self.classExpressions = [self.classExpressions] if self.classExpressions is not None else []
        self.classExpressions = [v if isinstance(v, ExistentialRestrictionExpression) else ExistentialRestrictionExpression(**as_dict(v)) for v in self.classExpressions]

        if self.unionEquivalentTo is not None and not isinstance(self.unionEquivalentTo, OboIdentifierString):
            self.unionEquivalentTo = OboIdentifierString(self.unionEquivalentTo)

        if self.unionEquivalentToExpression is not None and not isinstance(self.unionEquivalentToExpression, ExistentialRestrictionExpression):
            self.unionEquivalentToExpression = ExistentialRestrictionExpression(**as_dict(self.unionEquivalentToExpression))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PropertyChainAxiom(Axiom):
    """
    An axiom that represents an OWL property chain, e.g. R <- R1 o ... o Rn
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OBOGRAPHS["PropertyChainAxiom"]
    class_class_curie: ClassVar[str] = "obographs:PropertyChainAxiom"
    class_name: ClassVar[str] = "PropertyChainAxiom"
    class_model_uri: ClassVar[URIRef] = OBOGRAPHS.PropertyChainAxiom

    predicateId: Optional[str] = None
    chainPredicateIds: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.predicateId is not None and not isinstance(self.predicateId, str):
            self.predicateId = str(self.predicateId)

        if not isinstance(self.chainPredicateIds, list):
            self.chainPredicateIds = [self.chainPredicateIds] if self.chainPredicateIds is not None else []
        self.chainPredicateIds = [v if isinstance(v, str) else str(v) for v in self.chainPredicateIds]

        super().__post_init__(**kwargs)


# Enumerations
class ScopeEnum(EnumDefinitionImpl):
    """
    A vocabulary of terms that can be used to "scope" a synonym
    """
    hasExactSynonym = PermissibleValue(
        text="hasExactSynonym",
        description="The synonym represents the exact meaning of the node.",
        meaning=OIO["hasExactSynonym"])
    hasNarrowSynonym = PermissibleValue(
        text="hasNarrowSynonym",
        description="The synonym represents something narrower in meaning than the node.",
        meaning=OIO["hasNarrowSynonym"])
    hasBroadSynonym = PermissibleValue(
        text="hasBroadSynonym",
        description="The synonym represents something broader in meaning than the node.",
        meaning=OIO["hasBroadSynonym"])
    hasRelatedSynonym = PermissibleValue(
        text="hasRelatedSynonym",
        description="""The synonym represents something closely related in meaning than the node, but in not exact, broad, or narrow.""",
        meaning=OIO["hasRelatedSynonym"])

    _defn = EnumDefinition(
        name="ScopeEnum",
        description="A vocabulary of terms that can be used to \"scope\" a synonym",
    )

class NodeTypeEnum(EnumDefinitionImpl):
    """
    The main type of a node
    """
    CLASS = PermissibleValue(
        text="CLASS",
        meaning=OWL["Class"])
    PROPERTY = PermissibleValue(
        text="PROPERTY",
        meaning=RDFS["Property"])
    INDIVIDUAL = PermissibleValue(
        text="INDIVIDUAL",
        meaning=OWL["NamedIndividual"])

    _defn = EnumDefinition(
        name="NodeTypeEnum",
        description="The main type of a node",
    )

class PropertyTypeEnum(EnumDefinitionImpl):
    """
    The node subtype for property nodes
    """
    ANNOTATION = PermissibleValue(
        text="ANNOTATION",
        meaning=OWL["AnnotationProperty"])
    OBJECT = PermissibleValue(
        text="OBJECT",
        meaning=OWL["ObjectProperty"])
    DATA = PermissibleValue(
        text="DATA",
        meaning=OWL["DatatypeProperty"])

    _defn = EnumDefinition(
        name="PropertyTypeEnum",
        description="The node subtype for property nodes",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=OBOGRAPHS.id, name="id", curie=OBOGRAPHS.curie('id'),
                   model_uri=OBOGRAPHS.id, domain=None, range=URIRef)

slots.sub = Slot(uri=RDF.subject, name="sub", curie=RDF.curie('subject'),
                   model_uri=OBOGRAPHS.sub, domain=None, range=Optional[str])

slots.pred = Slot(uri=RDF.predicate, name="pred", curie=RDF.curie('predicate'),
                   model_uri=OBOGRAPHS.pred, domain=None, range=Optional[str])

slots.obj = Slot(uri=RDF.object, name="obj", curie=RDF.curie('object'),
                   model_uri=OBOGRAPHS.obj, domain=None, range=Optional[str])

slots.val = Slot(uri=RDF.object, name="val", curie=RDF.curie('object'),
                   model_uri=OBOGRAPHS.val, domain=None, range=Optional[str])

slots.valType = Slot(uri=OBOGRAPHS.valType, name="valType", curie=OBOGRAPHS.curie('valType'),
                   model_uri=OBOGRAPHS.valType, domain=None, range=Optional[str])

slots.lang = Slot(uri=OBOGRAPHS.lang, name="lang", curie=OBOGRAPHS.curie('lang'),
                   model_uri=OBOGRAPHS.lang, domain=None, range=Optional[str])

slots.lbl = Slot(uri=RDFS.label, name="lbl", curie=RDFS.curie('label'),
                   model_uri=OBOGRAPHS.lbl, domain=None, range=Optional[str])

slots.type = Slot(uri=OBOGRAPHS.type, name="type", curie=OBOGRAPHS.curie('type'),
                   model_uri=OBOGRAPHS.type, domain=None, range=Optional[str])

slots.propertyType = Slot(uri=OBOGRAPHS.propertyType, name="propertyType", curie=OBOGRAPHS.curie('propertyType'),
                   model_uri=OBOGRAPHS.propertyType, domain=None, range=Optional[Union[str, "PropertyTypeEnum"]])

slots.meta = Slot(uri=OBOGRAPHS.meta, name="meta", curie=OBOGRAPHS.curie('meta'),
                   model_uri=OBOGRAPHS.meta, domain=None, range=Optional[Union[dict, Meta]])

slots.definition = Slot(uri=IAO['0000115'], name="definition", curie=IAO.curie('0000115'),
                   model_uri=OBOGRAPHS.definition, domain=None, range=Optional[Union[dict, DefinitionPropertyValue]])

slots.basicPropertyValues = Slot(uri=OBOGRAPHS.basicPropertyValues, name="basicPropertyValues", curie=OBOGRAPHS.curie('basicPropertyValues'),
                   model_uri=OBOGRAPHS.basicPropertyValues, domain=None, range=Optional[Union[Union[dict, BasicPropertyValue], List[Union[dict, BasicPropertyValue]]]])

slots.comments = Slot(uri=RDFS.comment, name="comments", curie=RDFS.curie('comment'),
                   model_uri=OBOGRAPHS.comments, domain=None, range=Optional[Union[str, List[str]]])

slots.version = Slot(uri=OWL.versionInfo, name="version", curie=OWL.curie('versionInfo'),
                   model_uri=OBOGRAPHS.version, domain=None, range=Optional[str])

slots.deprecated = Slot(uri=OWL.deprecated, name="deprecated", curie=OWL.curie('deprecated'),
                   model_uri=OBOGRAPHS.deprecated, domain=None, range=Optional[Union[bool, Bool]])

slots.subsets = Slot(uri=OIO.inSubset, name="subsets", curie=OIO.curie('inSubset'),
                   model_uri=OBOGRAPHS.subsets, domain=None, range=Optional[Union[str, List[str]]])

slots.xrefs = Slot(uri=OBOGRAPHS.xrefs, name="xrefs", curie=OBOGRAPHS.curie('xrefs'),
                   model_uri=OBOGRAPHS.xrefs, domain=None, range=Optional[Union[Union[str, XrefString], List[Union[str, XrefString]]]])

slots.nodes = Slot(uri=OBOGRAPHS.nodes, name="nodes", curie=OBOGRAPHS.curie('nodes'),
                   model_uri=OBOGRAPHS.nodes, domain=None, range=Optional[Union[Dict[Union[str, NodeId], Union[dict, Node]], List[Union[dict, Node]]]])

slots.edges = Slot(uri=OBOGRAPHS.edges, name="edges", curie=OBOGRAPHS.curie('edges'),
                   model_uri=OBOGRAPHS.edges, domain=None, range=Optional[Union[Union[dict, Edge], List[Union[dict, Edge]]]])

slots.equivalentNodesSets = Slot(uri=OBOGRAPHS.equivalentNodesSets, name="equivalentNodesSets", curie=OBOGRAPHS.curie('equivalentNodesSets'),
                   model_uri=OBOGRAPHS.equivalentNodesSets, domain=None, range=Optional[Union[Union[dict, EquivalentNodesSet], List[Union[dict, EquivalentNodesSet]]]])

slots.logicalDefinitionAxioms = Slot(uri=OBOGRAPHS.logicalDefinitionAxioms, name="logicalDefinitionAxioms", curie=OBOGRAPHS.curie('logicalDefinitionAxioms'),
                   model_uri=OBOGRAPHS.logicalDefinitionAxioms, domain=None, range=Optional[Union[Union[dict, LogicalDefinitionAxiom], List[Union[dict, LogicalDefinitionAxiom]]]])

slots.disjointClassExpressionsAxioms = Slot(uri=OBOGRAPHS.disjointClassExpressionsAxioms, name="disjointClassExpressionsAxioms", curie=OBOGRAPHS.curie('disjointClassExpressionsAxioms'),
                   model_uri=OBOGRAPHS.disjointClassExpressionsAxioms, domain=None, range=Optional[Union[Union[dict, DisjointClassExpressionsAxiom], List[Union[dict, DisjointClassExpressionsAxiom]]]])

slots.domainRangeAxioms = Slot(uri=OBOGRAPHS.domainRangeAxioms, name="domainRangeAxioms", curie=OBOGRAPHS.curie('domainRangeAxioms'),
                   model_uri=OBOGRAPHS.domainRangeAxioms, domain=None, range=Optional[Union[Union[dict, DomainRangeAxiom], List[Union[dict, DomainRangeAxiom]]]])

slots.allValuesFromEdges = Slot(uri=OBOGRAPHS.allValuesFromEdges, name="allValuesFromEdges", curie=OBOGRAPHS.curie('allValuesFromEdges'),
                   model_uri=OBOGRAPHS.allValuesFromEdges, domain=None, range=Optional[Union[Union[dict, Edge], List[Union[dict, Edge]]]])

slots.propertyChainAxioms = Slot(uri=OBOGRAPHS.propertyChainAxioms, name="propertyChainAxioms", curie=OBOGRAPHS.curie('propertyChainAxioms'),
                   model_uri=OBOGRAPHS.propertyChainAxioms, domain=None, range=Optional[Union[Union[dict, PropertyChainAxiom], List[Union[dict, PropertyChainAxiom]]]])

slots.representativeNodeId = Slot(uri=OBOGRAPHS.representativeNodeId, name="representativeNodeId", curie=OBOGRAPHS.curie('representativeNodeId'),
                   model_uri=OBOGRAPHS.representativeNodeId, domain=None, range=Optional[str])

slots.chainPredicateIds = Slot(uri=OBOGRAPHS.chainPredicateIds, name="chainPredicateIds", curie=OBOGRAPHS.curie('chainPredicateIds'),
                   model_uri=OBOGRAPHS.chainPredicateIds, domain=None, range=Optional[Union[str, List[str]]])

slots.nodeIds = Slot(uri=OBOGRAPHS.nodeIds, name="nodeIds", curie=OBOGRAPHS.curie('nodeIds'),
                   model_uri=OBOGRAPHS.nodeIds, domain=None, range=Optional[Union[str, List[str]]])

slots.fillerId = Slot(uri=OBOGRAPHS.fillerId, name="fillerId", curie=OBOGRAPHS.curie('fillerId'),
                   model_uri=OBOGRAPHS.fillerId, domain=None, range=Optional[str])

slots.propertyId = Slot(uri=OBOGRAPHS.propertyId, name="propertyId", curie=OBOGRAPHS.curie('propertyId'),
                   model_uri=OBOGRAPHS.propertyId, domain=None, range=Optional[str])

slots.predicateId = Slot(uri=OBOGRAPHS.predicateId, name="predicateId", curie=OBOGRAPHS.curie('predicateId'),
                   model_uri=OBOGRAPHS.predicateId, domain=None, range=Optional[str])

slots.domainClassIds = Slot(uri=OBOGRAPHS.domainClassIds, name="domainClassIds", curie=OBOGRAPHS.curie('domainClassIds'),
                   model_uri=OBOGRAPHS.domainClassIds, domain=None, range=Optional[Union[str, List[str]]])

slots.rangeClassIds = Slot(uri=OBOGRAPHS.rangeClassIds, name="rangeClassIds", curie=OBOGRAPHS.curie('rangeClassIds'),
                   model_uri=OBOGRAPHS.rangeClassIds, domain=None, range=Optional[Union[str, List[str]]])

slots.synonyms = Slot(uri=OBOGRAPHS.synonyms, name="synonyms", curie=OBOGRAPHS.curie('synonyms'),
                   model_uri=OBOGRAPHS.synonyms, domain=None, range=Optional[Union[Union[dict, SynonymPropertyValue], List[Union[dict, SynonymPropertyValue]]]])

slots.synonymType = Slot(uri=OBOGRAPHS.synonymType, name="synonymType", curie=OBOGRAPHS.curie('synonymType'),
                   model_uri=OBOGRAPHS.synonymType, domain=None, range=Optional[Union[str, SynonymTypeIdentifierString]])

slots.isExact = Slot(uri=OBOGRAPHS.isExact, name="isExact", curie=OBOGRAPHS.curie('isExact'),
                   model_uri=OBOGRAPHS.isExact, domain=None, range=Optional[Union[bool, Bool]])

slots.graphs = Slot(uri=OBOGRAPHS.graphs, name="graphs", curie=OBOGRAPHS.curie('graphs'),
                   model_uri=OBOGRAPHS.graphs, domain=None, range=Optional[Union[Dict[Union[str, GraphId], Union[dict, Graph]], List[Union[dict, Graph]]]])

slots.prefixes = Slot(uri=SH.declare, name="prefixes", curie=SH.curie('declare'),
                   model_uri=OBOGRAPHS.prefixes, domain=None, range=Optional[Union[Dict[Union[str, PrefixDeclarationPrefix], Union[dict, PrefixDeclaration]], List[Union[dict, PrefixDeclaration]]]])

slots.synonymTypeDefinitions = Slot(uri=OBOGRAPHS.synonymTypeDefinitions, name="synonymTypeDefinitions", curie=OBOGRAPHS.curie('synonymTypeDefinitions'),
                   model_uri=OBOGRAPHS.synonymTypeDefinitions, domain=None, range=Optional[Union[Dict[Union[str, SynonymTypeDefinitionId], Union[dict, SynonymTypeDefinition]], List[Union[dict, SynonymTypeDefinition]]]])

slots.subsetDefinitions = Slot(uri=OBOGRAPHS.subsetDefinitions, name="subsetDefinitions", curie=OBOGRAPHS.curie('subsetDefinitions'),
                   model_uri=OBOGRAPHS.subsetDefinitions, domain=None, range=Optional[Union[Dict[Union[str, SubsetDefinitionId], Union[dict, SubsetDefinition]], List[Union[dict, SubsetDefinition]]]])

slots.prefixDeclaration__prefix = Slot(uri=SH.prefix, name="prefixDeclaration__prefix", curie=SH.curie('prefix'),
                   model_uri=OBOGRAPHS.prefixDeclaration__prefix, domain=None, range=URIRef)

slots.prefixDeclaration__namespace = Slot(uri=SH.namespace, name="prefixDeclaration__namespace", curie=SH.curie('namespace'),
                   model_uri=OBOGRAPHS.prefixDeclaration__namespace, domain=None, range=Optional[Union[str, URI]])

slots.logicalDefinitionAxiom__definedClassId = Slot(uri=OBOGRAPHS.definedClassId, name="logicalDefinitionAxiom__definedClassId", curie=OBOGRAPHS.curie('definedClassId'),
                   model_uri=OBOGRAPHS.logicalDefinitionAxiom__definedClassId, domain=None, range=Union[str, OboIdentifierString])

slots.logicalDefinitionAxiom__genusIds = Slot(uri=OBOGRAPHS.genusIds, name="logicalDefinitionAxiom__genusIds", curie=OBOGRAPHS.curie('genusIds'),
                   model_uri=OBOGRAPHS.logicalDefinitionAxiom__genusIds, domain=None, range=Optional[Union[Union[str, OboIdentifierString], List[Union[str, OboIdentifierString]]]])

slots.logicalDefinitionAxiom__restrictions = Slot(uri=OWL.someValuesFrom, name="logicalDefinitionAxiom__restrictions", curie=OWL.curie('someValuesFrom'),
                   model_uri=OBOGRAPHS.logicalDefinitionAxiom__restrictions, domain=None, range=Optional[Union[Union[dict, ExistentialRestrictionExpression], List[Union[dict, ExistentialRestrictionExpression]]]])

slots.disjointClassExpressionsAxiom__classIds = Slot(uri=OBOGRAPHS.classIds, name="disjointClassExpressionsAxiom__classIds", curie=OBOGRAPHS.curie('classIds'),
                   model_uri=OBOGRAPHS.disjointClassExpressionsAxiom__classIds, domain=None, range=Optional[Union[Union[str, OboIdentifierString], List[Union[str, OboIdentifierString]]]])

slots.disjointClassExpressionsAxiom__classExpressions = Slot(uri=OBOGRAPHS.classExpressions, name="disjointClassExpressionsAxiom__classExpressions", curie=OBOGRAPHS.curie('classExpressions'),
                   model_uri=OBOGRAPHS.disjointClassExpressionsAxiom__classExpressions, domain=None, range=Optional[Union[Union[dict, ExistentialRestrictionExpression], List[Union[dict, ExistentialRestrictionExpression]]]])

slots.disjointClassExpressionsAxiom__unionEquivalentTo = Slot(uri=OBOGRAPHS.unionEquivalentTo, name="disjointClassExpressionsAxiom__unionEquivalentTo", curie=OBOGRAPHS.curie('unionEquivalentTo'),
                   model_uri=OBOGRAPHS.disjointClassExpressionsAxiom__unionEquivalentTo, domain=None, range=Optional[Union[str, OboIdentifierString]])

slots.disjointClassExpressionsAxiom__unionEquivalentToExpression = Slot(uri=OBOGRAPHS.unionEquivalentToExpression, name="disjointClassExpressionsAxiom__unionEquivalentToExpression", curie=OBOGRAPHS.curie('unionEquivalentToExpression'),
                   model_uri=OBOGRAPHS.disjointClassExpressionsAxiom__unionEquivalentToExpression, domain=None, range=Optional[Union[dict, ExistentialRestrictionExpression]])

slots.Edge_sub = Slot(uri=RDF.subject, name="Edge_sub", curie=RDF.curie('subject'),
                   model_uri=OBOGRAPHS.Edge_sub, domain=Edge, range=str)

slots.Edge_pred = Slot(uri=RDF.predicate, name="Edge_pred", curie=RDF.curie('predicate'),
                   model_uri=OBOGRAPHS.Edge_pred, domain=Edge, range=str)

slots.Edge_obj = Slot(uri=RDF.object, name="Edge_obj", curie=RDF.curie('object'),
                   model_uri=OBOGRAPHS.Edge_obj, domain=Edge, range=str)

slots.Meta_xrefs = Slot(uri=OBOGRAPHS.xrefs, name="Meta_xrefs", curie=OBOGRAPHS.curie('xrefs'),
                   model_uri=OBOGRAPHS.Meta_xrefs, domain=Meta, range=Optional[Union[Union[dict, "XrefPropertyValue"], List[Union[dict, "XrefPropertyValue"]]]])

slots.DefinitionPropertyValue_val = Slot(uri=RDF.object, name="DefinitionPropertyValue_val", curie=RDF.curie('object'),
                   model_uri=OBOGRAPHS.DefinitionPropertyValue_val, domain=DefinitionPropertyValue, range=Optional[str])

slots.DefinitionPropertyValue_xrefs = Slot(uri=OBOGRAPHS.xrefs, name="DefinitionPropertyValue_xrefs", curie=OBOGRAPHS.curie('xrefs'),
                   model_uri=OBOGRAPHS.DefinitionPropertyValue_xrefs, domain=DefinitionPropertyValue, range=Optional[Union[Union[str, XrefString], List[Union[str, XrefString]]]])

slots.XrefPropertyValue_val = Slot(uri=RDF.object, name="XrefPropertyValue_val", curie=RDF.curie('object'),
                   model_uri=OBOGRAPHS.XrefPropertyValue_val, domain=XrefPropertyValue, range=Optional[str])

slots.SynonymPropertyValue_pred = Slot(uri=RDF.predicate, name="SynonymPropertyValue_pred", curie=RDF.curie('predicate'),
                   model_uri=OBOGRAPHS.SynonymPropertyValue_pred, domain=SynonymPropertyValue, range=Optional[Union[str, "ScopeEnum"]])

slots.SynonymPropertyValue_val = Slot(uri=RDF.object, name="SynonymPropertyValue_val", curie=RDF.curie('object'),
                   model_uri=OBOGRAPHS.SynonymPropertyValue_val, domain=SynonymPropertyValue, range=Optional[str])
