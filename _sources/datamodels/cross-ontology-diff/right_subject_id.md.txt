# Slot: right_subject_id
_The subject (child) of the matched/right edge, if matchable_


URI: [https://w3id.org/linkml/text_annotator/right_subject_id](https://w3id.org/linkml/text_annotator/right_subject_id)




## Inheritance

* **right_subject_id** [ right_side subject]





## Properties

* Range: [EntityReference](EntityReference.md)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Specification

<details>
```yaml
name: right_subject_id
description: The subject (child) of the matched/right edge, if matchable
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- right_side
- subject
alias: right_subject_id
domain_of:
- RelationalDiff
range: EntityReference

```
</details>