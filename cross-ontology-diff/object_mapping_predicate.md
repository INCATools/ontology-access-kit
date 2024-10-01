

# Slot: object_mapping_predicate


_The mapping predicate that holds between left_object_id and right_object_id_





URI: [xodiff:object_mapping_predicate](https://w3id.org/oak/cross-ontology-diff/object_mapping_predicate)




## Inheritance

* **object_mapping_predicate** [ [subject](subject.md) [predicate](predicate.md)]






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
| self | xodiff:object_mapping_predicate |
| native | xodiff:object_mapping_predicate |




## LinkML Source

<details>
```yaml
name: object_mapping_predicate
description: The mapping predicate that holds between left_object_id and right_object_id
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- subject
- predicate
alias: object_mapping_predicate
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference

```
</details>