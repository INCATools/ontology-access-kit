

# Slot: cosine_similarity


_the dot product of two node embeddings divided by the product of their lengths_





URI: [sim:cosine_similarity](https://w3id.org/linkml/similarity/cosine_similarity)




## Inheritance

* [score](score.md)
    * **cosine_similarity**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TermPairwiseSimilarity](TermPairwiseSimilarity.md) | A simple pairwise similarity between two atomic concepts/terms |  no  |







## Properties

* Range: [Float](Float.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:cosine_similarity |
| native | sim:cosine_similarity |




## LinkML Source

<details>
```yaml
name: cosine_similarity
description: the dot product of two node embeddings divided by the product of their
  lengths
from_schema: https://w3id.org/oak/similarity
rank: 1000
is_a: score
alias: cosine_similarity
domain_of:
- TermPairwiseSimilarity
range: float

```
</details>