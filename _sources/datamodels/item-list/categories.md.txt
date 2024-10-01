

# Slot: categories


_Controlled terms used to categorize an element._





URI: [dcterms:subject](http://purl.org/dc/terms/subject)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ItemList](ItemList.md) | a list of entities plus metadata |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Multivalued: True





## Comments

* if you wish to use uncontrolled terms or terms that lack identifiers then use the keywords element

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/item-list




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcterms:subject |
| native | itemList:categories |




## LinkML Source

<details>
```yaml
name: categories
description: Controlled terms used to categorize an element.
comments:
- if you wish to use uncontrolled terms or terms that lack identifiers then use the
  keywords element
from_schema: https://w3id.org/oak/item-list
rank: 1000
singular_name: category
slot_uri: dcterms:subject
alias: categories
owner: ItemList
domain_of:
- ItemList
range: uriorcurie
multivalued: true

```
</details>