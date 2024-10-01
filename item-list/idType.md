

# Slot: idType


_The type of the identifier. For example, if the id is a symbol, this would be 'symbol'_





URI: [itemList:idType](https://w3id.org/linkml/item-list/idType)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ListItem](ListItem.md) | an item in an item list |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)






## Examples

| Value |
| --- |
| biolink:symbol |
| skos:prefLabel |
| schema:identifier |

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | itemList:idType |
| native | itemList:idType |




## LinkML Source

<details>
```yaml
name: idType
description: The type of the identifier. For example, if the id is a symbol, this
  would be 'symbol'
examples:
- value: biolink:symbol
- value: skos:prefLabel
- value: schema:identifier
from_schema: https://w3id.org/oak/item-list
rank: 1000
alias: idType
owner: ListItem
domain_of:
- ListItem
range: uriorcurie

```
</details>