# Slot: search_terms
_An individual search term. The syntax is determined by the syntax slot_


URI: [search:search_terms](https://w3id.org/linkml/search_datamodel/search_terms)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[SearchBaseConfiguration](SearchBaseConfiguration.md) | A user-specified configuration that determines how a particular search operation works






## Properties

* Range: [SearchTerm](SearchTerm.md)
* Multivalued: True







## Alias




## Comments

* This slot is optional when the configuration is used to paramterize multiple searches
* If multiple terms are provided this is treated as a union query

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/search_datamodel




## LinkML Source

<details>
```yaml
name: search_terms
description: An individual search term. The syntax is determined by the syntax slot
comments:
- This slot is optional when the configuration is used to paramterize multiple searches
- If multiple terms are provided this is treated as a union query
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
multivalued: true
alias: search_terms
owner: SearchBaseConfiguration
domain_of:
- SearchBaseConfiguration
range: SearchTerm

```
</details>