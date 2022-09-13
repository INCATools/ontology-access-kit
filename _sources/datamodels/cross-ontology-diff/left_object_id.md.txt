# Slot: left_object_id
_The object (parent) of the source/left edge_


URI: [https://w3id.org/linkml/text_annotator/left_object_id](https://w3id.org/linkml/text_annotator/left_object_id)




## Inheritance

* **left_object_id** [ left_side object]





## Properties

* Range: [EntityReference](EntityReference.md)
* Multivalued: None



* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Specification

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
domain_of:
- RelationalDiff
range: EntityReference
required: true

```
</details>