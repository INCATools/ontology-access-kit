# Slot: left_predicate_id
_The predicate (relation) of the source/left edge_


URI: [https://w3id.org/linkml/text_annotator/left_predicate_id](https://w3id.org/linkml/text_annotator/left_predicate_id)




## Inheritance

* **left_predicate_id** [ [left_side](left_side.md) [predicate](predicate.md)]





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
name: left_predicate_id
description: The predicate (relation) of the source/left edge
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- left_side
- predicate
alias: left_predicate_id
domain_of:
- RelationalDiff
range: EntityReference
required: true

```
</details>