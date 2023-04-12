# Auto generated from input_specification.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-04-10T09:39:06
# Schema: inputspec
#
# id: https://w3id.org/oaklib/input-specification
# description: A data model for representing a set of inputs to OAK
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
from linkml_runtime.linkml_model.types import String
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
DCTERMS = CurieNamespace("dcterms", "http://purl.org/dc/terms/")
ITEMLIST = CurieNamespace("itemList", "https://w3id.org/linkml/item-list/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
DEFAULT_ = ITEMLIST


# Types


# Class references
class ResourceId(extended_str):
    pass


class OntologyResourceId(ResourceId):
    pass


class AssociationResourceId(ResourceId):
    pass


@dataclass
class InputSpecification(YAMLRoot):
    """
    input spec
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ITEMLIST.InputSpecification
    class_class_curie: ClassVar[str] = "itemList:InputSpecification"
    class_name: ClassVar[str] = "InputSpecification"
    class_model_uri: ClassVar[URIRef] = ITEMLIST.InputSpecification

    ontology_resources: Optional[
        Union[
            Dict[Union[str, OntologyResourceId], Union[dict, "OntologyResource"]],
            List[Union[dict, "OntologyResource"]],
        ]
    ] = empty_dict()
    association_resources: Optional[
        Union[
            Dict[Union[str, AssociationResourceId], Union[dict, "AssociationResource"]],
            List[Union[dict, "AssociationResource"]],
        ]
    ] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(
            slot_name="ontology_resources", slot_type=OntologyResource, key_name="id", keyed=True
        )

        self._normalize_inlined_as_dict(
            slot_name="association_resources",
            slot_type=AssociationResource,
            key_name="id",
            keyed=True,
        )

        super().__post_init__(**kwargs)


@dataclass
class Resource(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ITEMLIST.Resource
    class_class_curie: ClassVar[str] = "itemList:Resource"
    class_name: ClassVar[str] = "Resource"
    class_model_uri: ClassVar[URIRef] = ITEMLIST.Resource

    id: Union[str, ResourceId] = None
    path: Optional[str] = None
    format: Optional[str] = None
    selector: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ResourceId):
            self.id = ResourceId(self.id)

        if self.path is not None and not isinstance(self.path, str):
            self.path = str(self.path)

        if self.format is not None and not isinstance(self.format, str):
            self.format = str(self.format)

        if self.selector is not None and not isinstance(self.selector, str):
            self.selector = str(self.selector)

        super().__post_init__(**kwargs)


@dataclass
class OntologyResource(Resource):
    """
    A resource that points to an ontology
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ITEMLIST.OntologyResource
    class_class_curie: ClassVar[str] = "itemList:OntologyResource"
    class_name: ClassVar[str] = "OntologyResource"
    class_model_uri: ClassVar[URIRef] = ITEMLIST.OntologyResource

    id: Union[str, OntologyResourceId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OntologyResourceId):
            self.id = OntologyResourceId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class AssociationResource(Resource):
    """
    A resource that points to a set of associations
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ITEMLIST.AssociationResource
    class_class_curie: ClassVar[str] = "itemList:AssociationResource"
    class_name: ClassVar[str] = "AssociationResource"
    class_model_uri: ClassVar[URIRef] = ITEMLIST.AssociationResource

    id: Union[str, AssociationResourceId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AssociationResourceId):
            self.id = AssociationResourceId(self.id)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.inputSpecification__ontology_resources = Slot(
    uri=ITEMLIST.ontology_resources,
    name="inputSpecification__ontology_resources",
    curie=ITEMLIST.curie("ontology_resources"),
    model_uri=ITEMLIST.inputSpecification__ontology_resources,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, OntologyResourceId], Union[dict, OntologyResource]],
            List[Union[dict, OntologyResource]],
        ]
    ],
)

slots.inputSpecification__association_resources = Slot(
    uri=ITEMLIST.association_resources,
    name="inputSpecification__association_resources",
    curie=ITEMLIST.curie("association_resources"),
    model_uri=ITEMLIST.inputSpecification__association_resources,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, AssociationResourceId], Union[dict, AssociationResource]],
            List[Union[dict, AssociationResource]],
        ]
    ],
)

slots.resource__id = Slot(
    uri=ITEMLIST.id,
    name="resource__id",
    curie=ITEMLIST.curie("id"),
    model_uri=ITEMLIST.resource__id,
    domain=None,
    range=URIRef,
)

slots.resource__path = Slot(
    uri=ITEMLIST.path,
    name="resource__path",
    curie=ITEMLIST.curie("path"),
    model_uri=ITEMLIST.resource__path,
    domain=None,
    range=Optional[str],
)

slots.resource__format = Slot(
    uri=ITEMLIST.format,
    name="resource__format",
    curie=ITEMLIST.curie("format"),
    model_uri=ITEMLIST.resource__format,
    domain=None,
    range=Optional[str],
)

slots.resource__selector = Slot(
    uri=ITEMLIST.selector,
    name="resource__selector",
    curie=ITEMLIST.curie("selector"),
    model_uri=ITEMLIST.resource__selector,
    domain=None,
    range=Optional[str],
)
