

# Slot: elementId


_The identifier of the item. Note this can be a 'proper' CURIE ID or any other unique field, for example symbol_

__





URI: [itemList:elementId](https://w3id.org/linkml/item-list/elementId)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ListItem](ListItem.md) | an item in an item list |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | itemList:elementId |
| native | itemList:elementId |




## LinkML Source

<details>
```yaml
name: elementId
description: 'The identifier of the item. Note this can be a ''proper'' CURIE ID or
  any other unique field, for example symbol

  '
from_schema: https://w3id.org/oak/item-list
rank: 1000
key: true
alias: elementId
owner: ListItem
domain_of:
- ListItem
range: string
required: true

```
</details>