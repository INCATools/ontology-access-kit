

# Slot: additionalType


_An additional type for the item, typically used for adding more specific types from external vocabularies in microdata syntax. This is a relationship between something and a class that the thing is in. In RDFa syntax, it is better to use the native RDFa syntax - the 'typeof' attribute - for multiple types. Schema.org tools may have only weaker understanding of extra types, in particular those defined externally._





URI: [schema:additionalType](http://schema.org/additionalType)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemList](ItemList.md) | a list of entities plus metadata |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | schema:additionalType |
| native | itemList:additionalType |




## LinkML Source

<details>
```yaml
name: additionalType
description: An additional type for the item, typically used for adding more specific
  types from external vocabularies in microdata syntax. This is a relationship between
  something and a class that the thing is in. In RDFa syntax, it is better to use
  the native RDFa syntax - the 'typeof' attribute - for multiple types. Schema.org
  tools may have only weaker understanding of extra types, in particular those defined
  externally.
from_schema: https://w3id.org/oak/item-list
rank: 1000
slot_uri: schema:additionalType
alias: additionalType
owner: ItemList
domain_of:
- ItemList
range: uriorcurie
multivalued: true

```
</details>