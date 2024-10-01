

# Slot: subject_id


_The first of the two entities being compared_





URI: [sssom:subject_id](http://w3id.org/sssom/subject_id)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TermPairwiseSimilarity](TermPairwiseSimilarity.md) | A simple pairwise similarity between two atomic concepts/terms |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sssom:subject_id |
| native | sim:subject_id |




## LinkML Source

<details>
```yaml
name: subject_id
description: The first of the two entities being compared
from_schema: https://w3id.org/oak/similarity
rank: 1000
slot_uri: sssom:subject_id
alias: subject_id
domain_of:
- TermPairwiseSimilarity
range: uriorcurie
required: true

```
</details>