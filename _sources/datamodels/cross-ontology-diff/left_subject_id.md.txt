# Slot: left_subject_id
_The subject (child) of the source/left edge_


URI: [https://w3id.org/linkml/text_annotator/left_subject_id](https://w3id.org/linkml/text_annotator/left_subject_id)




## Inheritance

* **left_subject_id** [ left_side subject]





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
name: left_subject_id
description: The subject (child) of the source/left edge
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- left_side
- subject
alias: left_subject_id
domain_of:
- RelationalDiff
range: EntityReference
required: true

```
</details>