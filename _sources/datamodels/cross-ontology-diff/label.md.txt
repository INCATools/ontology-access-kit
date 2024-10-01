

# Slot: label


_human readable label_





URI: [rdfs:label](http://www.w3.org/2000/01/rdf-schema#label)



<!-- no inheritance hierarchy -->







## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [left_subject_label](left_subject_label.md) | The name of the subject (child) of the source/left edge | Label |  |
| [left_object_label](left_object_label.md) | The name of the object (parent) of the source/left edge | Label |  |
| [left_predicate_label](left_predicate_label.md) | The name of the predicate of the source/left edge | Label |  |
| [right_subject_label](right_subject_label.md) | The name of the subject (child) of the matched/right edge, if matchable | Label |  |
| [right_object_label](right_object_label.md) | The name of the object (parent) of the matched/right edge, if matchable | Label |  |
| [right_predicate_labels](right_predicate_labels.md) | The names corresponding to the right_predicate_ids | Label |  |



## Properties

* Range: [Label](Label.md)

* Mixin: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:label |
| native | xodiff:label |




## LinkML Source

<details>
```yaml
name: label
description: human readable label
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixin: true
slot_uri: rdfs:label
alias: label
range: Label

```
</details>