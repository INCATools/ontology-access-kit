

# Slot: right_object_id


_The object (parent) of the matched/right edge, if matchable_





URI: [xodiff:right_object_id](https://w3id.org/oak/cross-ontology-diff/right_object_id)




## Inheritance

* **right_object_id** [ [right_side](right_side.md) [object](object.md)]






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
| self | xodiff:right_object_id |
| native | xodiff:right_object_id |




## LinkML Source

<details>
```yaml
name: right_object_id
description: The object (parent) of the matched/right edge, if matchable
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- right_side
- object
alias: right_object_id
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference

```
</details>