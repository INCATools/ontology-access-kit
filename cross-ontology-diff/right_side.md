

# Slot: right_side


_The second ontology is arbitrarily designated the right side_





URI: [xodiff:right_side](https://w3id.org/oak/cross-ontology-diff/right_side)




## Inheritance

* [side](side.md)
    * **right_side**








## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [right_subject_id](right_subject_id.md) | The subject (child) of the matched/right edge, if matchable | EntityReference |  |
| [right_object_id](right_object_id.md) | The object (parent) of the matched/right edge, if matchable | EntityReference |  |
| [right_predicate_ids](right_predicate_ids.md) | * If the match type is consistent, then all consistent predicates | EntityReference |  |
| [right_subject_label](right_subject_label.md) | The name of the subject (child) of the matched/right edge, if matchable | Label |  |
| [right_object_label](right_object_label.md) | The name of the object (parent) of the matched/right edge, if matchable | Label |  |
| [right_predicate_labels](right_predicate_labels.md) | The names corresponding to the right_predicate_ids | Label |  |



## Properties

* Range: [String](String.md)

* Mixin: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | xodiff:right_side |
| native | xodiff:right_side |




## LinkML Source

<details>
```yaml
name: right_side
description: The second ontology is arbitrarily designated the right side
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
is_a: side
mixin: true
alias: right_side
range: string

```
</details>