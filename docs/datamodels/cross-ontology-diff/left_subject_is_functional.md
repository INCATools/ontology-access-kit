

# Slot: left_subject_is_functional


_True if a subject mapping is present, and maps uniquely within the same ontology_





URI: [xodiff:left_subject_is_functional](https://w3id.org/oak/cross-ontology-diff/left_subject_is_functional)




## Inheritance

* **left_subject_is_functional** [ [left_side](left_side.md) [is_functional](is_functional.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a... |  no  |







## Properties

* Range: [Boolean](Boolean.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | xodiff:left_subject_is_functional |
| native | xodiff:left_subject_is_functional |




## LinkML Source

<details>
```yaml
name: left_subject_is_functional
description: True if a subject mapping is present, and maps uniquely within the same
  ontology
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- left_side
- is_functional
alias: left_subject_is_functional
owner: RelationalDiff
domain_of:
- RelationalDiff
range: boolean

```
</details>