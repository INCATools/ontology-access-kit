# Slot: phenodigm_score
_the geometric mean of the jaccard similarity and the information content_


URI: [https://w3id.org/linkml/similarity/phenodigm_score](https://w3id.org/linkml/similarity/phenodigm_score)




## Inheritance

* [score](score.md)
    * **phenodigm_score**





## Properties

* Range: [NonNegativeFloat](NonNegativeFloat.md)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/similarity




## LinkML Specification

<details>
```yaml
name: phenodigm_score
description: the geometric mean of the jaccard similarity and the information content
from_schema: https://w3id.org/linkml/similarity
rank: 1000
is_a: score
alias: phenodigm_score
domain_of:
- TermPairwiseSimilarity
range: NonNegativeFloat
equals_expression: sqrt({jaccard_similarity} * {information_content})

```
</details>