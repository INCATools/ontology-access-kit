

# Slot: subject


_The child node on left or right side_





URI: [rdf:subject](http://www.w3.org/1999/02/22-rdf-syntax-ns#subject)



<!-- no inheritance hierarchy -->







## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [left_subject_id](left_subject_id.md) | The subject (child) of the source/left edge | EntityReference |  |
| [left_subject_label](left_subject_label.md) | The name of the subject (child) of the source/left edge | Label |  |
| [right_subject_id](right_subject_id.md) | The subject (child) of the matched/right edge, if matchable | EntityReference |  |
| [right_subject_label](right_subject_label.md) | The name of the subject (child) of the matched/right edge, if matchable | Label |  |
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
| self | rdf:subject |
| native | xodiff:subject |




## LinkML Source

<details>
```yaml
name: subject
description: The child node on left or right side
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixin: true
slot_uri: rdf:subject
alias: subject
range: string

```
</details>