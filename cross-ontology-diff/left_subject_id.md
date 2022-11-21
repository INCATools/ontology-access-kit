# Slot: left_subject_id
_The subject (child) of the source/left edge_


URI: [ann:left_subject_id](https://w3id.org/linkml/text_annotator/left_subject_id)




## Inheritance

* **left_subject_id** [ [left_side](left_side.md) [subject](subject.md)]





## Applicable Classes

| Name | Description |
| --- | --- |
[RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a...






## Properties

* Range: [EntityReference](EntityReference.md)
* Required: True








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Source

<details>
```yaml
name: left_subject_id
description: The subject (child) of the source/left edge
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- left_side
- subject
alias: left_subject_id
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference
required: true

```
</details>