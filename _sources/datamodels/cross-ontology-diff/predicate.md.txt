

# Slot: predicate


_The relationship type between subject and object on left or right side_





URI: [rdf:predicate](http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate)



<!-- no inheritance hierarchy -->







## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [left_predicate_id](left_predicate_id.md) | The predicate (relation) of the source/left edge | EntityReference |  |
| [left_predicate_label](left_predicate_label.md) | The name of the predicate of the source/left edge | Label |  |
| [right_predicate_ids](right_predicate_ids.md) | * If the match type is consistent, then all consistent predicates | EntityReference |  |
| [right_predicate_labels](right_predicate_labels.md) | The names corresponding to the right_predicate_ids | Label |  |
| [subject_mapping_predicate](subject_mapping_predicate.md) | The mapping predicate that holds between left_subject_id and right_subject_id | EntityReference |  |
| [object_mapping_predicate](object_mapping_predicate.md) | The mapping predicate that holds between left_object_id and right_object_id | EntityReference |  |



## Properties

* Range: [String](String.md)

* Mixin: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:predicate |
| native | xodiff:predicate |




## LinkML Source

<details>
```yaml
name: predicate
description: The relationship type between subject and object on left or right side
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixin: true
slot_uri: rdf:predicate
alias: predicate
range: string

```
</details>