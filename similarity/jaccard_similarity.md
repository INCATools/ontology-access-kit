

# Slot: jaccard_similarity


_The number of concepts in the intersection divided by the number in the union_





URI: [sim:jaccard_similarity](https://w3id.org/linkml/similarity/jaccard_similarity)




## Inheritance

* [score](score.md)
    * **jaccard_similarity**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TermPairwiseSimilarity](TermPairwiseSimilarity.md) | A simple pairwise similarity between two atomic concepts/terms |  no  |







## Properties

* Range: [ZeroToOne](ZeroToOne.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:jaccard_similarity |
| native | sim:jaccard_similarity |




## LinkML Source

<details>
```yaml
name: jaccard_similarity
description: The number of concepts in the intersection divided by the number in the
  union
from_schema: https://w3id.org/oak/similarity
rank: 1000
is_a: score
alias: jaccard_similarity
domain_of:
- TermPairwiseSimilarity
range: ZeroToOne

```
</details>