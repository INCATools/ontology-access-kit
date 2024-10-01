

# Slot: wasGeneratedBy


_The provenance of the list, for example a script that generated the list_





URI: [prov:wasGeneratedBy](http://www.w3.org/ns/prov#wasGeneratedBy)



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
| self | prov:wasGeneratedBy |
| native | itemList:wasGeneratedBy |




## LinkML Source

<details>
```yaml
name: wasGeneratedBy
description: The provenance of the list, for example a script that generated the list
from_schema: https://w3id.org/oak/item-list
rank: 1000
slot_uri: prov:wasGeneratedBy
alias: wasGeneratedBy
owner: ItemList
domain_of:
- ItemList
range: uriorcurie
multivalued: true

```
</details>