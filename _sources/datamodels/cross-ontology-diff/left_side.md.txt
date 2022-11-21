# Slot: left_side
_The first ontology is arbitrarily designated the left side_


URI: [ann:left_side](https://w3id.org/linkml/text_annotator/left_side)




## Inheritance

* [side](side.md)
    * **left_side**






## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [left_subject_id](left_subject_id.md) | The subject (child) of the source/left edge | EntityReference |  |
| [left_object_id](left_object_id.md) | The object (parent) of the source/left edge | EntityReference |  |
| [left_predicate_id](left_predicate_id.md) | The predicate (relation) of the source/left edge | EntityReference |  |
| [left_subject_label](left_subject_label.md) | The name of the subject (child) of the source/left edge | Label |  |
| [left_object_label](left_object_label.md) | The name of the object (parent) of the source/left edge | Label |  |
| [left_predicate_label](left_predicate_label.md) | The name of the predicate of the source/left edge | Label |  |
| [left_subject_is_functional](left_subject_is_functional.md) | True if a subject mapping is present, and maps uniquely within the same ontol... | None |  |
| [left_object_is_functional](left_object_is_functional.md) | True if an object mapping is present, and maps uniquely within the same ontol... | None |  |



## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Mixin: True








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Source

<details>
```yaml
name: left_side
description: The first ontology is arbitrarily designated the left side
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
is_a: side
mixin: true
alias: left_side
range: string

```
</details>