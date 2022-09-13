# Slot: right_subject_label
_The name of the subject (child) of the matched/right edge, if matchable_


URI: [https://w3id.org/linkml/text_annotator/right_subject_label](https://w3id.org/linkml/text_annotator/right_subject_label)




## Inheritance

* **right_subject_label** [ right_side subject label]





## Properties

* Range: [Label](Label.md)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Specification

<details>
```yaml
name: right_subject_label
description: The name of the subject (child) of the matched/right edge, if matchable
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
mixins:
- right_side
- subject
- label
alias: right_subject_label
domain_of:
- RelationalDiff
range: Label

```
</details>