

# Slot: itemListElements


_The entities in the list, represented as a simple list_





URI: [schema:itemListElement](http://schema.org/itemListElement)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemList](ItemList.md) | a list of entities plus metadata |  no  |







## Properties

* Range: [ListItem](ListItem.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | schema:itemListElement |
| native | itemList:itemListElements |




## LinkML Source

<details>
```yaml
name: itemListElements
description: The entities in the list, represented as a simple list
from_schema: https://w3id.org/oak/item-list
rank: 1000
singular_name: itemListElement
slot_uri: schema:itemListElement
alias: itemListElements
owner: ItemList
domain_of:
- ItemList
range: ListItem
multivalued: true
inlined: false

```
</details>