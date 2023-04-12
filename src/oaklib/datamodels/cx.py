# Auto generated from cx.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-04-09T14:06:51
# Schema: cx
#
# id: https://w3id.org/oaklib/cx
# description: NDEX CX datamodel
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
from linkml_runtime.linkml_model.types import Float, Integer, String
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import bnode, empty_dict, empty_list
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
CX = CurieNamespace("cx", "https://w3id.org/oaklib/cx/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
DEFAULT_ = CX


# Types


# Class references
class DescriptorBlockCXVersion(extended_float):
    pass


@dataclass
class DescriptorBlock(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.DescriptorBlock
    class_class_curie: ClassVar[str] = "cx:DescriptorBlock"
    class_name: ClassVar[str] = "DescriptorBlock"
    class_model_uri: ClassVar[URIRef] = CX.DescriptorBlock

    CXVersion: Union[float, DescriptorBlockCXVersion] = None
    hasFragments: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.CXVersion):
            self.MissingRequiredField("CXVersion")
        if not isinstance(self.CXVersion, DescriptorBlockCXVersion):
            self.CXVersion = DescriptorBlockCXVersion(self.CXVersion)

        if self.hasFragments is not None and not isinstance(self.hasFragments, int):
            self.hasFragments = int(self.hasFragments)

        super().__post_init__(**kwargs)


@dataclass
class MetaDatum(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.MetaDatum
    class_class_curie: ClassVar[str] = "cx:MetaDatum"
    class_name: ClassVar[str] = "MetaDatum"
    class_model_uri: ClassVar[URIRef] = CX.MetaDatum

    elementCount: Optional[int] = None
    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.elementCount is not None and not isinstance(self.elementCount, int):
            self.elementCount = int(self.elementCount)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass
class MetadataBlock(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.MetadataBlock
    class_class_curie: ClassVar[str] = "cx:MetadataBlock"
    class_name: ClassVar[str] = "MetadataBlock"
    class_model_uri: ClassVar[URIRef] = CX.MetadataBlock

    metaData: Optional[Union[Union[dict, MetaDatum], List[Union[dict, MetaDatum]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.metaData, list):
            self.metaData = [self.metaData] if self.metaData is not None else []
        self.metaData = [
            v if isinstance(v, MetaDatum) else MetaDatum(**as_dict(v)) for v in self.metaData
        ]

        super().__post_init__(**kwargs)


@dataclass
class IsTreeEdge(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.IsTreeEdge
    class_class_curie: ClassVar[str] = "cx:IsTreeEdge"
    class_name: ClassVar[str] = "IsTreeEdge"
    class_model_uri: ClassVar[URIRef] = CX.IsTreeEdge

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class Interaction(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Interaction
    class_class_curie: ClassVar[str] = "cx:Interaction"
    class_name: ClassVar[str] = "Interaction"
    class_model_uri: ClassVar[URIRef] = CX.Interaction

    a: Optional[str] = None
    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.a is not None and not isinstance(self.a, str):
            self.a = str(self.a)

        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class Name(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Name
    class_class_curie: ClassVar[str] = "cx:Name"
    class_name: ClassVar[str] = "Name"
    class_model_uri: ClassVar[URIRef] = CX.Name

    d: Optional[str] = None
    a: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        if self.a is not None and not isinstance(self.a, str):
            self.a = str(self.a)

        super().__post_init__(**kwargs)


@dataclass
class Edge(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Edge
    class_class_curie: ClassVar[str] = "cx:Edge"
    class_name: ClassVar[str] = "Edge"
    class_model_uri: ClassVar[URIRef] = CX.Edge

    Is_Tree_Edge: Optional[str] = None
    interaction: Optional[str] = None
    name: Optional[str] = None
    id: Optional[int] = None
    s: Optional[int] = None
    t: Optional[int] = None
    v: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.Is_Tree_Edge is not None and not isinstance(self.Is_Tree_Edge, str):
            self.Is_Tree_Edge = str(self.Is_Tree_Edge)

        if self.interaction is not None and not isinstance(self.interaction, str):
            self.interaction = str(self.interaction)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.id is not None and not isinstance(self.id, int):
            self.id = int(self.id)

        if self.s is not None and not isinstance(self.s, int):
            self.s = int(self.s)

        if self.t is not None and not isinstance(self.t, int):
            self.t = int(self.t)

        if self.v is not None and not isinstance(self.v, str):
            self.v = str(self.v)

        super().__post_init__(**kwargs)


@dataclass
class Description(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Description
    class_class_curie: ClassVar[str] = "cx:Description"
    class_name: ClassVar[str] = "Description"
    class_model_uri: ClassVar[URIRef] = CX.Description

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class NetworkAttribute(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.NetworkAttribute
    class_class_curie: ClassVar[str] = "cx:NetworkAttribute"
    class_name: ClassVar[str] = "NetworkAttribute"
    class_model_uri: ClassVar[URIRef] = CX.NetworkAttribute

    name: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class Size(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Size
    class_class_curie: ClassVar[str] = "cx:Size"
    class_name: ClassVar[str] = "Size"
    class_model_uri: ClassVar[URIRef] = CX.Size

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class AlignFdr(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.AlignFdr
    class_class_curie: ClassVar[str] = "cx:AlignFdr"
    class_name: ClassVar[str] = "AlignFdr"
    class_model_uri: ClassVar[URIRef] = CX.AlignFdr

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class AlignGoID(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.AlignGoID
    class_class_curie: ClassVar[str] = "cx:AlignGoID"
    class_name: ClassVar[str] = "AlignGoID"
    class_model_uri: ClassVar[URIRef] = CX.AlignGoID

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class AlignScore(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.AlignScore
    class_class_curie: ClassVar[str] = "cx:AlignScore"
    class_name: ClassVar[str] = "AlignScore"
    class_model_uri: ClassVar[URIRef] = CX.AlignScore

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class Annot(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Annot
    class_class_curie: ClassVar[str] = "cx:Annot"
    class_name: ClassVar[str] = "Annot"
    class_model_uri: ClassVar[URIRef] = CX.Annot

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class AnnotSource(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.AnnotSource
    class_class_curie: ClassVar[str] = "cx:AnnotSource"
    class_name: ClassVar[str] = "AnnotSource"
    class_model_uri: ClassVar[URIRef] = CX.AnnotSource

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class CcOverlap(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.CcOverlap
    class_class_curie: ClassVar[str] = "cx:CcOverlap"
    class_name: ClassVar[str] = "CcOverlap"
    class_model_uri: ClassVar[URIRef] = CX.CcOverlap

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class Gene(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Gene
    class_class_curie: ClassVar[str] = "cx:Gene"
    class_name: ClassVar[str] = "Gene"
    class_model_uri: ClassVar[URIRef] = CX.Gene

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class Jaccard(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Jaccard
    class_class_curie: ClassVar[str] = "cx:Jaccard"
    class_name: ClassVar[str] = "Jaccard"
    class_model_uri: ClassVar[URIRef] = CX.Jaccard

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class Overlap(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Overlap
    class_class_curie: ClassVar[str] = "cx:Overlap"
    class_name: ClassVar[str] = "Overlap"
    class_model_uri: ClassVar[URIRef] = CX.Overlap

    d: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.d is not None and not isinstance(self.d, str):
            self.d = str(self.d)

        super().__post_init__(**kwargs)


@dataclass
class Node(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.Node
    class_class_curie: ClassVar[str] = "cx:Node"
    class_name: ClassVar[str] = "Node"
    class_model_uri: ClassVar[URIRef] = CX.Node

    id: Optional[int] = None
    v: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, int):
            self.id = int(self.id)

        if self.v is not None and not isinstance(self.v, str):
            self.v = str(self.v)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.y is not None and not isinstance(self.y, float):
            self.y = float(self.y)

        super().__post_init__(**kwargs)


@dataclass
class AttributeDeclaration(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.AttributeDeclaration
    class_class_curie: ClassVar[str] = "cx:AttributeDeclaration"
    class_name: ClassVar[str] = "AttributeDeclaration"
    class_model_uri: ClassVar[URIRef] = CX.AttributeDeclaration

    edges: Optional[Union[Union[dict, Edge], List[Union[dict, Edge]]]] = empty_list()
    networkAttributes: Optional[str] = None
    nodes: Optional[Union[Union[dict, Node], List[Union[dict, Node]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.edges, list):
            self.edges = [self.edges] if self.edges is not None else []
        self.edges = [v if isinstance(v, Edge) else Edge(**as_dict(v)) for v in self.edges]

        if self.networkAttributes is not None and not isinstance(self.networkAttributes, str):
            self.networkAttributes = str(self.networkAttributes)

        if not isinstance(self.nodes, list):
            self.nodes = [self.nodes] if self.nodes is not None else []
        self.nodes = [v if isinstance(v, Node) else Node(**as_dict(v)) for v in self.nodes]

        super().__post_init__(**kwargs)


@dataclass
class AttributeDeclarationsBlock(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.AttributeDeclarationsBlock
    class_class_curie: ClassVar[str] = "cx:AttributeDeclarationsBlock"
    class_name: ClassVar[str] = "AttributeDeclarationsBlock"
    class_model_uri: ClassVar[URIRef] = CX.AttributeDeclarationsBlock

    attributeDeclarations: Optional[Union[dict, AttributeDeclaration]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.attributeDeclarations is not None and not isinstance(
            self.attributeDeclarations, AttributeDeclaration
        ):
            self.attributeDeclarations = AttributeDeclaration(**as_dict(self.attributeDeclarations))

        super().__post_init__(**kwargs)


@dataclass
class NetworkAttributesBlock(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.NetworkAttributesBlock
    class_class_curie: ClassVar[str] = "cx:NetworkAttributesBlock"
    class_name: ClassVar[str] = "NetworkAttributesBlock"
    class_model_uri: ClassVar[URIRef] = CX.NetworkAttributesBlock

    networkAttributes: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.networkAttributes is not None and not isinstance(self.networkAttributes, str):
            self.networkAttributes = str(self.networkAttributes)

        super().__post_init__(**kwargs)


@dataclass
class V(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.V
    class_class_curie: ClassVar[str] = "cx:V"
    class_name: ClassVar[str] = "V"
    class_model_uri: ClassVar[URIRef] = CX.V

    Size: Optional[str] = None
    align_fdr: Optional[str] = None
    align_score: Optional[str] = None
    annot: Optional[str] = None
    annot_source: Optional[str] = None
    cc_overlap: Optional[str] = None
    genes: Optional[str] = None
    jaccard: Optional[str] = None
    n: Optional[int] = None
    overlap: Optional[str] = None
    align_goID: Optional[str] = None
    Is_Tree_Edge: Optional[str] = None
    i: Optional[str] = None
    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.Size is not None and not isinstance(self.Size, str):
            self.Size = str(self.Size)

        if self.align_fdr is not None and not isinstance(self.align_fdr, str):
            self.align_fdr = str(self.align_fdr)

        if self.align_score is not None and not isinstance(self.align_score, str):
            self.align_score = str(self.align_score)

        if self.annot is not None and not isinstance(self.annot, str):
            self.annot = str(self.annot)

        if self.annot_source is not None and not isinstance(self.annot_source, str):
            self.annot_source = str(self.annot_source)

        if self.cc_overlap is not None and not isinstance(self.cc_overlap, str):
            self.cc_overlap = str(self.cc_overlap)

        if self.genes is not None and not isinstance(self.genes, str):
            self.genes = str(self.genes)

        if self.jaccard is not None and not isinstance(self.jaccard, str):
            self.jaccard = str(self.jaccard)

        if self.n is not None and not isinstance(self.n, int):
            self.n = int(self.n)

        if self.overlap is not None and not isinstance(self.overlap, str):
            self.overlap = str(self.overlap)

        if self.align_goID is not None and not isinstance(self.align_goID, str):
            self.align_goID = str(self.align_goID)

        if self.Is_Tree_Edge is not None and not isinstance(self.Is_Tree_Edge, str):
            self.Is_Tree_Edge = str(self.Is_Tree_Edge)

        if self.i is not None and not isinstance(self.i, str):
            self.i = str(self.i)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass
class NodesBlock(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.NodesBlock
    class_class_curie: ClassVar[str] = "cx:NodesBlock"
    class_name: ClassVar[str] = "NodesBlock"
    class_model_uri: ClassVar[URIRef] = CX.NodesBlock

    nodes: Optional[Union[Union[dict, Node], List[Union[dict, Node]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.nodes, list):
            self.nodes = [self.nodes] if self.nodes is not None else []
        self.nodes = [v if isinstance(v, Node) else Node(**as_dict(v)) for v in self.nodes]

        super().__post_init__(**kwargs)


@dataclass
class EdgesBlock(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.EdgesBlock
    class_class_curie: ClassVar[str] = "cx:EdgesBlock"
    class_name: ClassVar[str] = "EdgesBlock"
    class_model_uri: ClassVar[URIRef] = CX.EdgesBlock

    edges: Optional[Union[Union[dict, Edge], List[Union[dict, Edge]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.edges, list):
            self.edges = [self.edges] if self.edges is not None else []
        self.edges = [v if isinstance(v, Edge) else Edge(**as_dict(v)) for v in self.edges]

        super().__post_init__(**kwargs)


@dataclass
class CXDocument(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CX.CXDocument
    class_class_curie: ClassVar[str] = "cx:CXDocument"
    class_name: ClassVar[str] = "CXDocument"
    class_model_uri: ClassVar[URIRef] = CX.CXDocument

    descriptorBlock: Optional[str] = None
    metadataBlock: Optional[str] = None
    attributeDeclarationsBlock: Optional[str] = None
    networkAttributesBlock: Optional[str] = None
    nodesBlock: Optional[str] = None
    edgesBlock: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.descriptorBlock is not None and not isinstance(self.descriptorBlock, str):
            self.descriptorBlock = str(self.descriptorBlock)

        if self.metadataBlock is not None and not isinstance(self.metadataBlock, str):
            self.metadataBlock = str(self.metadataBlock)

        if self.attributeDeclarationsBlock is not None and not isinstance(
            self.attributeDeclarationsBlock, str
        ):
            self.attributeDeclarationsBlock = str(self.attributeDeclarationsBlock)

        if self.networkAttributesBlock is not None and not isinstance(
            self.networkAttributesBlock, str
        ):
            self.networkAttributesBlock = str(self.networkAttributesBlock)

        if self.nodesBlock is not None and not isinstance(self.nodesBlock, str):
            self.nodesBlock = str(self.nodesBlock)

        if self.edgesBlock is not None and not isinstance(self.edgesBlock, str):
            self.edgesBlock = str(self.edgesBlock)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.CXVersion = Slot(
    uri=CX.CXVersion,
    name="CXVersion",
    curie=CX.curie("CXVersion"),
    model_uri=CX.CXVersion,
    domain=None,
    range=URIRef,
)

slots.hasFragments = Slot(
    uri=CX.hasFragments,
    name="hasFragments",
    curie=CX.curie("hasFragments"),
    model_uri=CX.hasFragments,
    domain=None,
    range=Optional[int],
)

slots.elementCount = Slot(
    uri=CX.elementCount,
    name="elementCount",
    curie=CX.curie("elementCount"),
    model_uri=CX.elementCount,
    domain=None,
    range=Optional[int],
)

slots.name = Slot(
    uri=CX.name,
    name="name",
    curie=CX.curie("name"),
    model_uri=CX.name,
    domain=None,
    range=Optional[str],
)

slots.metaData = Slot(
    uri=CX.metaData,
    name="metaData",
    curie=CX.curie("metaData"),
    model_uri=CX.metaData,
    domain=None,
    range=Optional[Union[Union[dict, MetaDatum], List[Union[dict, MetaDatum]]]],
)

slots.d = Slot(
    uri=CX.d, name="d", curie=CX.curie("d"), model_uri=CX.d, domain=None, range=Optional[str]
)

slots.a = Slot(
    uri=CX.a, name="a", curie=CX.curie("a"), model_uri=CX.a, domain=None, range=Optional[str]
)

slots.Is_Tree_Edge = Slot(
    uri=CX.Is_Tree_Edge,
    name="Is_Tree_Edge",
    curie=CX.curie("Is_Tree_Edge"),
    model_uri=CX.Is_Tree_Edge,
    domain=None,
    range=Optional[str],
)

slots.interaction = Slot(
    uri=CX.interaction,
    name="interaction",
    curie=CX.curie("interaction"),
    model_uri=CX.interaction,
    domain=None,
    range=Optional[str],
)

slots.id = Slot(
    uri=CX.id, name="id", curie=CX.curie("id"), model_uri=CX.id, domain=None, range=Optional[int]
)

slots.s = Slot(
    uri=CX.s, name="s", curie=CX.curie("s"), model_uri=CX.s, domain=None, range=Optional[int]
)

slots.t = Slot(
    uri=CX.t, name="t", curie=CX.curie("t"), model_uri=CX.t, domain=None, range=Optional[int]
)

slots.v = Slot(
    uri=CX.v, name="v", curie=CX.curie("v"), model_uri=CX.v, domain=None, range=Optional[str]
)

slots.description = Slot(
    uri=CX.description,
    name="description",
    curie=CX.curie("description"),
    model_uri=CX.description,
    domain=None,
    range=Optional[str],
)

slots.Size = Slot(
    uri=CX.Size,
    name="Size",
    curie=CX.curie("Size"),
    model_uri=CX.Size,
    domain=None,
    range=Optional[str],
)

slots.align_fdr = Slot(
    uri=CX.align_fdr,
    name="align_fdr",
    curie=CX.curie("align_fdr"),
    model_uri=CX.align_fdr,
    domain=None,
    range=Optional[str],
)

slots.align_goID = Slot(
    uri=CX.align_goID,
    name="align_goID",
    curie=CX.curie("align_goID"),
    model_uri=CX.align_goID,
    domain=None,
    range=Optional[str],
)

slots.align_score = Slot(
    uri=CX.align_score,
    name="align_score",
    curie=CX.curie("align_score"),
    model_uri=CX.align_score,
    domain=None,
    range=Optional[str],
)

slots.annot = Slot(
    uri=CX.annot,
    name="annot",
    curie=CX.curie("annot"),
    model_uri=CX.annot,
    domain=None,
    range=Optional[str],
)

slots.annot_source = Slot(
    uri=CX.annot_source,
    name="annot_source",
    curie=CX.curie("annot_source"),
    model_uri=CX.annot_source,
    domain=None,
    range=Optional[str],
)

slots.cc_overlap = Slot(
    uri=CX.cc_overlap,
    name="cc_overlap",
    curie=CX.curie("cc_overlap"),
    model_uri=CX.cc_overlap,
    domain=None,
    range=Optional[str],
)

slots.genes = Slot(
    uri=CX.genes,
    name="genes",
    curie=CX.curie("genes"),
    model_uri=CX.genes,
    domain=None,
    range=Optional[str],
)

slots.jaccard = Slot(
    uri=CX.jaccard,
    name="jaccard",
    curie=CX.curie("jaccard"),
    model_uri=CX.jaccard,
    domain=None,
    range=Optional[str],
)

slots.overlap = Slot(
    uri=CX.overlap,
    name="overlap",
    curie=CX.curie("overlap"),
    model_uri=CX.overlap,
    domain=None,
    range=Optional[str],
)

slots.x = Slot(
    uri=CX.x, name="x", curie=CX.curie("x"), model_uri=CX.x, domain=None, range=Optional[float]
)

slots.y = Slot(
    uri=CX.y, name="y", curie=CX.curie("y"), model_uri=CX.y, domain=None, range=Optional[float]
)

slots.edges = Slot(
    uri=CX.edges,
    name="edges",
    curie=CX.curie("edges"),
    model_uri=CX.edges,
    domain=None,
    range=Optional[Union[Union[dict, Edge], List[Union[dict, Edge]]]],
)

slots.networkAttributes = Slot(
    uri=CX.networkAttributes,
    name="networkAttributes",
    curie=CX.curie("networkAttributes"),
    model_uri=CX.networkAttributes,
    domain=None,
    range=Optional[str],
)

slots.nodes = Slot(
    uri=CX.nodes,
    name="nodes",
    curie=CX.curie("nodes"),
    model_uri=CX.nodes,
    domain=None,
    range=Optional[Union[Union[dict, Node], List[Union[dict, Node]]]],
)

slots.attributeDeclarations = Slot(
    uri=CX.attributeDeclarations,
    name="attributeDeclarations",
    curie=CX.curie("attributeDeclarations"),
    model_uri=CX.attributeDeclarations,
    domain=None,
    range=Optional[Union[dict, AttributeDeclaration]],
)

slots.n = Slot(
    uri=CX.n, name="n", curie=CX.curie("n"), model_uri=CX.n, domain=None, range=Optional[int]
)

slots.i = Slot(
    uri=CX.i, name="i", curie=CX.curie("i"), model_uri=CX.i, domain=None, range=Optional[str]
)

slots.descriptorBlock = Slot(
    uri=CX.descriptorBlock,
    name="descriptorBlock",
    curie=CX.curie("descriptorBlock"),
    model_uri=CX.descriptorBlock,
    domain=None,
    range=Optional[str],
)

slots.metadataBlock = Slot(
    uri=CX.metadataBlock,
    name="metadataBlock",
    curie=CX.curie("metadataBlock"),
    model_uri=CX.metadataBlock,
    domain=None,
    range=Optional[str],
)

slots.attributeDeclarationsBlock = Slot(
    uri=CX.attributeDeclarationsBlock,
    name="attributeDeclarationsBlock",
    curie=CX.curie("attributeDeclarationsBlock"),
    model_uri=CX.attributeDeclarationsBlock,
    domain=None,
    range=Optional[str],
)

slots.networkAttributesBlock = Slot(
    uri=CX.networkAttributesBlock,
    name="networkAttributesBlock",
    curie=CX.curie("networkAttributesBlock"),
    model_uri=CX.networkAttributesBlock,
    domain=None,
    range=Optional[str],
)

slots.nodesBlock = Slot(
    uri=CX.nodesBlock,
    name="nodesBlock",
    curie=CX.curie("nodesBlock"),
    model_uri=CX.nodesBlock,
    domain=None,
    range=Optional[str],
)

slots.edgesBlock = Slot(
    uri=CX.edgesBlock,
    name="edgesBlock",
    curie=CX.curie("edgesBlock"),
    model_uri=CX.edgesBlock,
    domain=None,
    range=Optional[str],
)
