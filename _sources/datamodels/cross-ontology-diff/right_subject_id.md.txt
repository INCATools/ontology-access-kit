

# Slot: right_subject_id


_The subject (child) of the matched/right edge, if matchable_





URI: [xodiff:right_subject_id](https://w3id.org/oak/cross-ontology-diff/right_subject_id)




## Inheritance

* **right_subject_id** [ [right_side](right_side.md) [subject](subject.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a... |  no  |







## Properties

* Range: [EntityReference](EntityReference.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | xodiff:right_subject_id |
| native | xodiff:right_subject_id |




## LinkML Source

<details>
```yaml
name: right_subject_id
description: The subject (child) of the matched/right edge, if matchable
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- right_side
- subject
alias: right_subject_id
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference

```
</details>