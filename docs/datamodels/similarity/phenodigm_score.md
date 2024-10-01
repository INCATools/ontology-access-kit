

# Slot: phenodigm_score


_the geometric mean of the jaccard similarity and the information content_





URI: [sim:phenodigm_score](https://w3id.org/linkml/similarity/phenodigm_score)




## Inheritance

* [score](score.md)
    * **phenodigm_score**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TermPairwiseSimilarity](TermPairwiseSimilarity.md) | A simple pairwise similarity between two atomic concepts/terms |  no  |







## Properties

* Range: [NonNegativeFloat](NonNegativeFloat.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:phenodigm_score |
| native | sim:phenodigm_score |




## LinkML Source

<details>
```yaml
name: phenodigm_score
description: the geometric mean of the jaccard similarity and the information content
from_schema: https://w3id.org/oak/similarity
rank: 1000
is_a: score
alias: phenodigm_score
domain_of:
- TermPairwiseSimilarity
range: NonNegativeFloat
equals_expression: sqrt({jaccard_similarity} * {information_content})

```
</details>