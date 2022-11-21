# Slot: right_object_id
_The object (parent) of the matched/right edge, if matchable_


URI: [ann:right_object_id](https://w3id.org/linkml/text_annotator/right_object_id)




## Inheritance

* **right_object_id** [ [right_side](right_side.md) [object](object.md)]





## Applicable Classes

| Name | Description |
| --- | --- |
[RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a...






## Properties

* Range: [EntityReference](EntityReference.md)







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Source

<details>
```yaml
name: right_object_id
description: The object (parent) of the matched/right edge, if matchable
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- right_side
- object
alias: right_object_id
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference

```
</details>