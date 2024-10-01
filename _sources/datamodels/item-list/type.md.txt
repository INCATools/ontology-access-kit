

# Slot: type


_The type of the item._





URI: [itemList:type](https://w3id.org/linkml/item-list/type)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Thing](Thing.md) |  |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)






## Examples

| Value |
| --- |
| biolink:Gene |
| schema:Person |

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | itemList:type |
| native | itemList:type |




## LinkML Source

<details>
```yaml
name: type
description: The type of the item.
examples:
- value: biolink:Gene
- value: schema:Person
from_schema: https://w3id.org/oak/item-list
rank: 1000
alias: type
owner: Thing
domain_of:
- Thing
range: uriorcurie

```
</details>