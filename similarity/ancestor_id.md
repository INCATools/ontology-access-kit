

# Slot: ancestor_id


_the most recent common ancestor of the two compared entities. If there are multiple MRCAs then the most informative one is selected_





URI: [sim:ancestor_id](https://w3id.org/linkml/similarity/ancestor_id)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TermPairwiseSimilarity](TermPairwiseSimilarity.md) | A simple pairwise similarity between two atomic concepts/terms |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)





## TODOs

* decide on what to do when there are multiple possible ancestos

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:ancestor_id |
| native | sim:ancestor_id |




## LinkML Source

<details>
```yaml
name: ancestor_id
description: the most recent common ancestor of the two compared entities. If there
  are multiple MRCAs then the most informative one is selected
todos:
- decide on what to do when there are multiple possible ancestos
from_schema: https://w3id.org/oak/similarity
rank: 1000
alias: ancestor_id
domain_of:
- TermPairwiseSimilarity
range: uriorcurie

```
</details>