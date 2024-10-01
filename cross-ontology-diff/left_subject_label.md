

# Slot: left_subject_label


_The name of the subject (child) of the source/left edge_





URI: [xodiff:left_subject_label](https://w3id.org/oak/cross-ontology-diff/left_subject_label)




## Inheritance

* **left_subject_label** [ [left_side](left_side.md) [subject](subject.md) [label](label.md)]






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
| self | xodiff:left_subject_label |
| native | xodiff:left_subject_label |




## LinkML Source

<details>
```yaml
name: left_subject_label
description: The name of the subject (child) of the source/left edge
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- left_side
- subject
- label
alias: left_subject_label
owner: RelationalDiff
domain_of:
- RelationalDiff
range: Label

```
</details>