# Slot: ancestor_id
_the most recent common ancestor of the two compared entities. If there are multiple MRCAs then the most informative one is selected_


URI: [sim:ancestor_id](https://w3id.org/linkml/similarity/ancestor_id)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[TermPairwiseSimilarity](TermPairwiseSimilarity.md) | A simple pairwise similarity between two atomic concepts/terms






## Properties

* Range: [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)







## TODOs

* decide on what to do when there are multiple possible ancestos

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/similarity




## LinkML Source

<details>
```yaml
name: ancestor_id
description: the most recent common ancestor of the two compared entities. If there
  are multiple MRCAs then the most informative one is selected
todos:
- decide on what to do when there are multiple possible ancestos
from_schema: https://w3id.org/linkml/similarity
rank: 1000
alias: ancestor_id
domain_of:
- TermPairwiseSimilarity
range: uriorcurie

```
</details>