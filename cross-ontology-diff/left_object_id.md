# Slot: left_object_id
_The object (parent) of the source/left edge_


URI: [ann:left_object_id](https://w3id.org/linkml/text_annotator/left_object_id)




## Inheritance

* **left_object_id** [ [left_side](left_side.md) [object](object.md)]





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
name: left_object_id
description: The object (parent) of the source/left edge
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- left_side
- object
alias: left_object_id
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference
required: true

```
</details>