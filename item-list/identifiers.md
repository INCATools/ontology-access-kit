

# Slot: identifiers


_A list of identifiers for the item. For example, if the id is a symbol, this would be a list of identifiers for the item, such as HGNC, MGI, etc._





URI: [itemList:identifiers](https://w3id.org/linkml/item-list/identifiers)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Thing](Thing.md) |  |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | itemList:identifiers |
| native | itemList:identifiers |




## LinkML Source

<details>
```yaml
name: identifiers
description: A list of identifiers for the item. For example, if the id is a symbol,
  this would be a list of identifiers for the item, such as HGNC, MGI, etc.
from_schema: https://w3id.org/oak/item-list
rank: 1000
alias: identifiers
owner: Thing
domain_of:
- Thing
range: uriorcurie
multivalued: true

```
</details>