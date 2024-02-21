# Auto generated from item_list.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-04-13T19:34:47
# Schema: itemList
#
# id: https://w3id.org/oak/item-list
# description: A data model for representing simple lists of entities such as genes. The data model is based on
#              the schema.org ItemList class.
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
from linkml_runtime.linkml_model.types import Integer, String, Uri, Uriorcurie
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import (
    dataclasses_init_fn_with_kwargs,
)
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import (
    URI,
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
DCTERMS = CurieNamespace("dcterms", "http://purl.org/dc/terms/")
ITEMLIST = CurieNamespace("itemList", "https://w3id.org/linkml/item-list/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = CurieNamespace("rdfs", "http://example.org/UNKNOWN/rdfs/")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
DEFAULT_ = ITEMLIST


# Types


# Class references
class ListItemElementId(extended_str):
    pass


class ThingId(URIorCURIE):
    pass


@dataclass
class ItemListCollection(YAMLRoot):
    """
    a set of item lists
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ITEMLIST.ItemListCollection
    class_class_curie: ClassVar[str] = "itemList:ItemListCollection"
    class_name: ClassVar[str] = "ItemListCollection"
    class_model_uri: ClassVar[URIRef] = ITEMLIST.ItemListCollection

    itemLists: Optional[Union[Union[dict, "ItemList"], List[Union[dict, "ItemList"]]]] = (
        empty_list()
    )

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.itemLists, list):
            self.itemLists = [self.itemLists] if self.itemLists is not None else []
        self.itemLists = [
            v if isinstance(v, ItemList) else ItemList(**as_dict(v)) for v in self.itemLists
        ]

        super().__post_init__(**kwargs)


@dataclass
class ItemList(YAMLRoot):
    """
    a list of entities plus metadata
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.ItemList
    class_class_curie: ClassVar[str] = "schema:ItemList"
    class_name: ClassVar[str] = "ItemList"
    class_model_uri: ClassVar[URIRef] = ITEMLIST.ItemList

    id: Optional[Union[str, URIorCURIE]] = None
    name: Optional[str] = None
    description: Optional[str] = None
    itemListElements: Optional[
        Union[Union[str, ListItemElementId], List[Union[str, ListItemElementId]]]
    ] = empty_list()
    numberOfItems: Optional[Union[str, "ItemListOrderType"]] = None
    itemMetadataMap: Optional[
        Union[
            Dict[Union[str, ListItemElementId], Union[dict, "ListItem"]],
            List[Union[dict, "ListItem"]],
        ]
    ] = empty_dict()
    categories: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    keywords: Optional[Union[str, List[str]]] = empty_list()
    additionalType: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = (
        empty_list()
    )
    wasGeneratedBy: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = (
        empty_list()
    )

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, URIorCURIE):
            self.id = URIorCURIE(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.itemListElements, list):
            self.itemListElements = (
                [self.itemListElements] if self.itemListElements is not None else []
            )
        self.itemListElements = [
            v if isinstance(v, ListItemElementId) else ListItemElementId(v)
            for v in self.itemListElements
        ]

        if self.numberOfItems is not None and not isinstance(self.numberOfItems, ItemListOrderType):
            self.numberOfItems = ItemListOrderType(self.numberOfItems)

        self._normalize_inlined_as_dict(
            slot_name="itemMetadataMap", slot_type=ListItem, key_name="elementId", keyed=True
        )

        if not isinstance(self.categories, list):
            self.categories = [self.categories] if self.categories is not None else []
        self.categories = [
            v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.categories
        ]

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        if not isinstance(self.additionalType, list):
            self.additionalType = [self.additionalType] if self.additionalType is not None else []
        self.additionalType = [
            v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.additionalType
        ]

        if not isinstance(self.wasGeneratedBy, list):
            self.wasGeneratedBy = [self.wasGeneratedBy] if self.wasGeneratedBy is not None else []
        self.wasGeneratedBy = [
            v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.wasGeneratedBy
        ]

        super().__post_init__(**kwargs)


@dataclass
class ListItem(YAMLRoot):
    """
    an item in an item list
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.ListItem
    class_class_curie: ClassVar[str] = "schema:ListItem"
    class_name: ClassVar[str] = "ListItem"
    class_model_uri: ClassVar[URIRef] = ITEMLIST.ListItem

    elementId: Union[str, ListItemElementId] = None
    idType: Optional[Union[str, URIorCURIE]] = None
    item: Optional[Union[dict, "Thing"]] = None
    position: Optional[int] = None
    previousItem: Optional[Union[str, ListItemElementId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.elementId):
            self.MissingRequiredField("elementId")
        if not isinstance(self.elementId, ListItemElementId):
            self.elementId = ListItemElementId(self.elementId)

        if self.idType is not None and not isinstance(self.idType, URIorCURIE):
            self.idType = URIorCURIE(self.idType)

        if self.item is not None and not isinstance(self.item, Thing):
            self.item = Thing(**as_dict(self.item))

        if self.position is not None and not isinstance(self.position, int):
            self.position = int(self.position)

        if self.previousItem is not None and not isinstance(self.previousItem, ListItemElementId):
            self.previousItem = ListItemElementId(self.previousItem)

        super().__post_init__(**kwargs)


@dataclass
class Thing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.Thing
    class_class_curie: ClassVar[str] = "schema:Thing"
    class_name: ClassVar[str] = "Thing"
    class_model_uri: ClassVar[URIRef] = ITEMLIST.Thing

    id: Union[str, ThingId] = None
    name: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    identifiers: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = (
        empty_list()
    )
    description: Optional[str] = None
    type: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ThingId):
            self.id = ThingId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if not isinstance(self.identifiers, list):
            self.identifiers = [self.identifiers] if self.identifiers is not None else []
        self.identifiers = [
            v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.identifiers
        ]

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.type is not None and not isinstance(self.type, URIorCURIE):
            self.type = URIorCURIE(self.type)

        super().__post_init__(**kwargs)


# Enumerations
class ItemListOrderType(EnumDefinitionImpl):
    """
    The order of the items in the list
    """

    Ascending = PermissibleValue(
        text="Ascending",
        description="The items are ordered in ascending order",
        meaning=SCHEMA.ItemListOrderAscending,
    )
    Descending = PermissibleValue(
        text="Descending",
        description="The items are ordered in descending order",
        meaning=SCHEMA.ItemListOrderDescending,
    )
    Unordered = PermissibleValue(
        text="Unordered", description="The items are unordered", meaning=SCHEMA.ItemListUnordered
    )

    _defn = EnumDefinition(
        name="ItemListOrderType",
        description="The order of the items in the list",
    )


# Slots
class slots:
    pass


slots.itemListCollection__itemLists = Slot(
    uri=ITEMLIST.itemLists,
    name="itemListCollection__itemLists",
    curie=ITEMLIST.curie("itemLists"),
    model_uri=ITEMLIST.itemListCollection__itemLists,
    domain=None,
    range=Optional[Union[Union[dict, ItemList], List[Union[dict, ItemList]]]],
)

slots.itemList__id = Slot(
    uri=ITEMLIST.id,
    name="itemList__id",
    curie=ITEMLIST.curie("id"),
    model_uri=ITEMLIST.itemList__id,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.itemList__name = Slot(
    uri=ITEMLIST.name,
    name="itemList__name",
    curie=ITEMLIST.curie("name"),
    model_uri=ITEMLIST.itemList__name,
    domain=None,
    range=Optional[str],
)

slots.itemList__description = Slot(
    uri=ITEMLIST.description,
    name="itemList__description",
    curie=ITEMLIST.curie("description"),
    model_uri=ITEMLIST.itemList__description,
    domain=None,
    range=Optional[str],
)

slots.itemList__itemListElements = Slot(
    uri=SCHEMA.itemListElement,
    name="itemList__itemListElements",
    curie=SCHEMA.curie("itemListElement"),
    model_uri=ITEMLIST.itemList__itemListElements,
    domain=None,
    range=Optional[Union[Union[str, ListItemElementId], List[Union[str, ListItemElementId]]]],
)

slots.itemList__numberOfItems = Slot(
    uri=SCHEMA.numberOfItems,
    name="itemList__numberOfItems",
    curie=SCHEMA.curie("numberOfItems"),
    model_uri=ITEMLIST.itemList__numberOfItems,
    domain=None,
    range=Optional[Union[str, "ItemListOrderType"]],
)

slots.itemList__itemMetadataMap = Slot(
    uri=ITEMLIST.itemMetadataMap,
    name="itemList__itemMetadataMap",
    curie=ITEMLIST.curie("itemMetadataMap"),
    model_uri=ITEMLIST.itemList__itemMetadataMap,
    domain=None,
    range=Optional[
        Union[
            Dict[Union[str, ListItemElementId], Union[dict, ListItem]], List[Union[dict, ListItem]]
        ]
    ],
)

slots.itemList__categories = Slot(
    uri=DCTERMS.subject,
    name="itemList__categories",
    curie=DCTERMS.curie("subject"),
    model_uri=ITEMLIST.itemList__categories,
    domain=None,
    range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]],
)

slots.itemList__keywords = Slot(
    uri=SCHEMA.keywords,
    name="itemList__keywords",
    curie=SCHEMA.curie("keywords"),
    model_uri=ITEMLIST.itemList__keywords,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.itemList__additionalType = Slot(
    uri=SCHEMA.additionalType,
    name="itemList__additionalType",
    curie=SCHEMA.curie("additionalType"),
    model_uri=ITEMLIST.itemList__additionalType,
    domain=None,
    range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]],
)

slots.itemList__wasGeneratedBy = Slot(
    uri=PROV.wasGeneratedBy,
    name="itemList__wasGeneratedBy",
    curie=PROV.curie("wasGeneratedBy"),
    model_uri=ITEMLIST.itemList__wasGeneratedBy,
    domain=None,
    range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]],
)

slots.listItem__elementId = Slot(
    uri=ITEMLIST.elementId,
    name="listItem__elementId",
    curie=ITEMLIST.curie("elementId"),
    model_uri=ITEMLIST.listItem__elementId,
    domain=None,
    range=URIRef,
)

slots.listItem__idType = Slot(
    uri=ITEMLIST.idType,
    name="listItem__idType",
    curie=ITEMLIST.curie("idType"),
    model_uri=ITEMLIST.listItem__idType,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.listItem__item = Slot(
    uri=SCHEMA.item,
    name="listItem__item",
    curie=SCHEMA.curie("item"),
    model_uri=ITEMLIST.listItem__item,
    domain=None,
    range=Optional[Union[dict, Thing]],
)

slots.listItem__position = Slot(
    uri=SCHEMA.position,
    name="listItem__position",
    curie=SCHEMA.curie("position"),
    model_uri=ITEMLIST.listItem__position,
    domain=None,
    range=Optional[int],
)

slots.listItem__previousItem = Slot(
    uri=SCHEMA.previousItem,
    name="listItem__previousItem",
    curie=SCHEMA.curie("previousItem"),
    model_uri=ITEMLIST.listItem__previousItem,
    domain=None,
    range=Optional[Union[str, ListItemElementId]],
)

slots.thing__id = Slot(
    uri=SCHEMA.identifier,
    name="thing__id",
    curie=SCHEMA.curie("identifier"),
    model_uri=ITEMLIST.thing__id,
    domain=None,
    range=URIRef,
)

slots.thing__name = Slot(
    uri=RDFS.label,
    name="thing__name",
    curie=RDFS.curie("label"),
    model_uri=ITEMLIST.thing__name,
    domain=None,
    range=Optional[str],
)

slots.thing__url = Slot(
    uri=ITEMLIST.url,
    name="thing__url",
    curie=ITEMLIST.curie("url"),
    model_uri=ITEMLIST.thing__url,
    domain=None,
    range=Optional[Union[str, URI]],
)

slots.thing__identifiers = Slot(
    uri=ITEMLIST.identifiers,
    name="thing__identifiers",
    curie=ITEMLIST.curie("identifiers"),
    model_uri=ITEMLIST.thing__identifiers,
    domain=None,
    range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]],
)

slots.thing__description = Slot(
    uri=ITEMLIST.description,
    name="thing__description",
    curie=ITEMLIST.curie("description"),
    model_uri=ITEMLIST.thing__description,
    domain=None,
    range=Optional[str],
)

slots.thing__type = Slot(
    uri=ITEMLIST.type,
    name="thing__type",
    curie=ITEMLIST.curie("type"),
    model_uri=ITEMLIST.thing__type,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)
