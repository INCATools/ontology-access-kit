

# Slot: object


_The object node on left or right side_





URI: [rdf:object](http://www.w3.org/1999/02/22-rdf-syntax-ns#object)



<!-- no inheritance hierarchy -->







## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [left_object_id](left_object_id.md) | The object (parent) of the source/left edge | EntityReference |  |
| [left_object_label](left_object_label.md) | The name of the object (parent) of the source/left edge | Label |  |
| [right_object_id](right_object_id.md) | The object (parent) of the matched/right edge, if matchable | EntityReference |  |
| [right_object_label](right_object_label.md) | The name of the object (parent) of the matched/right edge, if matchable | Label |  |



## Properties

* Range: [String](String.md)

* Mixin: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/cross-ontology-diff




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:object |
| native | xodiff:object |




## LinkML Source

<details>
```yaml
name: object
description: The object node on left or right side
from_schema: https://w3id.org/oak/cross-ontology-diff
rank: 1000
mixin: true
slot_uri: rdf:object
alias: object
range: string

```
</details>