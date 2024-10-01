

# Slot: right_subject_label


_The name of the subject (child) of the matched/right edge, if matchable_





URI: [xodiff:right_subject_label](https://w3id.org/oak/cross-ontology-diff/right_subject_label)




## Inheritance

* **right_subject_label** [ [right_side](right_side.md) [subject](subject.md) [label](label.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a... |  no  |







## Properties

* Range: [Label](Label.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | xodiff:right_subject_label |
| native | xodiff:right_subject_label |




## LinkML Source

<details>
```yaml
name: right_subject_label
description: The name of the subject (child) of the matched/right edge, if matchable
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- right_side
- subject
- label
alias: right_subject_label
owner: RelationalDiff
domain_of:
- RelationalDiff
range: Label

```
</details>