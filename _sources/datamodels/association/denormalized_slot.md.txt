

# Slot: denormalized_slot


_denormalized slots are for models that follow a denormalized data model_





URI: [ontoassoc:denormalized_slot](https://w3id.org/oak/association/denormalized_slot)



<!-- no inheritance hierarchy -->







## Mixin Usage

| mixed into | description | range | domain |
| --- | --- | --- | --- |
| [subject_label](subject_label.md) | The label of the thing which the association is about | string | PositiveOrNegativeAssociation |
| [predicate_label](predicate_label.md) | The label of the type of relationship between the subject and object | string | PositiveOrNegativeAssociation |
| [object_label](object_label.md) | The label of the ontology entity that is associated with the subject | string | PositiveOrNegativeAssociation |



## Properties

* Range: [String](String.md)

* Mixin: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:denormalized_slot |
| native | ontoassoc:denormalized_slot |




## LinkML Source

<details>
```yaml
name: denormalized_slot
description: denormalized slots are for models that follow a denormalized data model
from_schema: https://w3id.org/oak/association
rank: 1000
mixin: true
alias: denormalized_slot
range: string

```
</details>