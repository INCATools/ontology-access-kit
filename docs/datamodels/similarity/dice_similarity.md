

# Slot: dice_similarity



URI: [sim:dice_similarity](https://w3id.org/linkml/similarity/dice_similarity)




## Inheritance

* [score](score.md)
    * **dice_similarity**






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
| self | sim:dice_similarity |
| native | sim:dice_similarity |




## LinkML Source

<details>
```yaml
name: dice_similarity
from_schema: https://w3id.org/oak/similarity
rank: 1000
is_a: score
alias: dice_similarity
domain_of:
- TermPairwiseSimilarity
range: ZeroToOne

```
</details>