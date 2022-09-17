# Slot: right_side

URI: [https://w3id.org/linkml/text_annotator/right_side](https://w3id.org/linkml/text_annotator/right_side)




## Inheritance

* [side](side.md)
    * **right_side**




## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [right_subject_id](right_subject_id.md) | The subject (child) of the matched/right edge, if matchable | EntityReference |  |
| [right_object_id](right_object_id.md) | The object (parent) of the matched/right edge, if matchable | EntityReference |  |
| [right_predicate_ids](right_predicate_ids.md) | * If the match type is consistent, then all consistent predicates.
* If the match type is identical, then the identical predicate.
* If the match type is OtherRelationship, then all predicates that form a path between right subject and object | EntityReference |  |
| [right_subject_label](right_subject_label.md) | The name of the subject (child) of the matched/right edge, if matchable | Label |  |
| [right_object_label](right_object_label.md) | The name of the object (parent) of the matched/right edge, if matchable | Label |  |
| [right_predicate_labels](right_predicate_labels.md) | The names corresponding to the right_predicate_ids | Label |  |



## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: None




* Mixin: True




## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Specification

<details>
```yaml
name: right_side
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
is_a: side
mixin: true
alias: right_side
range: string

```
</details>