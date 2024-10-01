

# Slot: right_predicate_ids


_* If the match type is consistent, then all consistent predicates._

_* If the match type is identical, then the identical predicate._

_* If the match type is OtherRelationship, then all predicates that form a path between right subject and object_





URI: [xodiff:right_predicate_ids](https://w3id.org/oak/cross-ontology-diff/right_predicate_ids)




## Inheritance

* **right_predicate_ids** [ [right_side](right_side.md) [predicate](predicate.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a... |  no  |







## Properties

* Range: [EntityReference](EntityReference.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | xodiff:right_predicate_ids |
| native | xodiff:right_predicate_ids |




## LinkML Source

<details>
```yaml
name: right_predicate_ids
description: '* If the match type is consistent, then all consistent predicates.

  * If the match type is identical, then the identical predicate.

  * If the match type is OtherRelationship, then all predicates that form a path between
  right subject and object'
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- right_side
- predicate
alias: right_predicate_ids
owner: RelationalDiff
domain_of:
- RelationalDiff
range: EntityReference
multivalued: true

```
</details>