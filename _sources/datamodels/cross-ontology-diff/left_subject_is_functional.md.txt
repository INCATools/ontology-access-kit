# Slot: left_subject_is_functional
_True if a subject mapping is present, and maps uniquely within the same ontology_


URI: [https://w3id.org/linkml/text_annotator/left_subject_is_functional](https://w3id.org/linkml/text_annotator/left_subject_is_functional)




## Inheritance

* **left_subject_is_functional** [ left_side is_functional]





## Properties

* Range: [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Specification

<details>
```yaml
name: left_subject_is_functional
description: True if a subject mapping is present, and maps uniquely within the same
  ontology
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- left_side
- is_functional
alias: left_subject_is_functional
domain_of:
- RelationalDiff
range: boolean

```
</details>