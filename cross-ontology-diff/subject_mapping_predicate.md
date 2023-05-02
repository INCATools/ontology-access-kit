# Slot: subject_mapping_predicate


_The mapping predicate that holds between left_subject_id and right_subject_id_



URI: [xodiff:subject_mapping_predicate](https://w3id.org/oak/cross-ontology-diff/subject_mapping_predicate)




## Inheritance

* **subject_mapping_predicate** [ [subject](subject.md) [predicate](predicate.md)]





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a... |  no  |







## Properties

* Range: [EntityReference](EntityReference.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## LinkML Source

<details>
```yaml
name: subject_mapping_predicate
description: The mapping predicate that holds between left_subject_id and right_subject_id
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- subject
- predicate
alias: subject_mapping_predicate
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference

```
</details>