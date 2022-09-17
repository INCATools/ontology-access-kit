# Slot: right_object_id
_The object (parent) of the matched/right edge, if matchable_


URI: [https://w3id.org/linkml/text_annotator/right_object_id](https://w3id.org/linkml/text_annotator/right_object_id)




## Inheritance

* **right_object_id** [ right_side object]





## Properties

* Range: [EntityReference](EntityReference.md)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Specification

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
domain_of:
- RelationalDiff
range: EntityReference

```
</details>