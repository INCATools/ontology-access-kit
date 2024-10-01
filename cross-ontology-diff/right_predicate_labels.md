

# Slot: right_predicate_labels


_The names corresponding to the right_predicate_ids_





URI: [xodiff:right_predicate_labels](https://w3id.org/oak/cross-ontology-diff/right_predicate_labels)




## Inheritance

* **right_predicate_labels** [ [right_side](right_side.md) [predicate](predicate.md) [label](label.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [RelationalDiff](RelationalDiff.md) | A relational diff expresses the difference between an edge in one ontology, a... |  no  |







## Properties

* Range: [Label](Label.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | xodiff:right_predicate_labels |
| native | xodiff:right_predicate_labels |




## LinkML Source

<details>
```yaml
name: right_predicate_labels
description: The names corresponding to the right_predicate_ids
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixins:
- right_side
- predicate
- label
alias: right_predicate_labels
owner: RelationalDiff
domain_of:
- RelationalDiff
range: Label
multivalued: true

```
</details>