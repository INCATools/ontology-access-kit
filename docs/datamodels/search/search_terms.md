

# Slot: search_terms


_An individual search term. The syntax is determined by the syntax slot_





URI: [ontosearch:search_terms](https://w3id.org/oak/search-datamodel/search_terms)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SearchBaseConfiguration](SearchBaseConfiguration.md) | A user-specified configuration that determines how a particular search operat... |  no  |







## Properties

* Range: [SearchTerm](SearchTerm.md)

* Multivalued: True





## Comments

* This slot is optional when the configuration is used to parameterize multiple searches
* If multiple terms are provided this is treated as a union query

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/search-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontosearch:search_terms |
| native | ontosearch:search_terms |




## LinkML Source

<details>
```yaml
name: search_terms
description: An individual search term. The syntax is determined by the syntax slot
comments:
- This slot is optional when the configuration is used to parameterize multiple searches
- If multiple terms are provided this is treated as a union query
from_schema: https://w3id.org/oak/search-datamodel
rank: 1000
alias: search_terms
owner: SearchBaseConfiguration
domain_of:
- SearchBaseConfiguration
range: SearchTerm
multivalued: true

```
</details>