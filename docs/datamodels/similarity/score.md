# Slot: score
_Abstract base slot for different kinds of scores_


URI: [sim:score](https://w3id.org/linkml/similarity/score)




## Inheritance

* **score**
    * [information_content](information_content.md)
    * [jaccard_similarity](jaccard_similarity.md)
    * [dice_similarity](dice_similarity.md)
    * [phenodigm_score](phenodigm_score.md)
    * [overlap_coefficient](overlap_coefficient.md)
    * [subsumes_score](subsumes_score.md)
    * [subsumed_by_score](subsumed_by_score.md)
    * [intersection_count](intersection_count.md)
    * [union_count](union_count.md)





## Applicable Classes

| Name | Description |
| --- | --- |
[BestMatch](BestMatch.md) | 






## Properties

* Range: [String](String.md)







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## LinkML Source

<details>
```yaml
name: score
description: Abstract base slot for different kinds of scores
from_schema: https://w3id.org/oak/similarity
rank: 1000
abstract: true
alias: score
domain_of:
- BestMatch
range: string

```
</details>