# Slot: left_predicate_id
_The predicate (relation) of the source/left edge_


URI: [xodiff:left_predicate_id](https://w3id.org/oak/cross-ontology-diff/left_predicate_id)




## Inheritance

* **left_predicate_id** [ [left_side](left_side.md) [predicate](predicate.md)]





## Applicable Classes

| Name | Description |
| --- | --- |
[RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a...






## Properties

* Range: [EntityReference](EntityReference.md)
* Required: True








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## LinkML Source

<details>
```yaml
name: left_predicate_id
description: The predicate (relation) of the source/left edge
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- left_side
- predicate
alias: left_predicate_id
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference
required: true

```
</details>