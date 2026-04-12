

# Slot: object_label


_The label of the ontology entity that is associated with the subject._





URI: [sssom:object_label](https://w3id.org/sssom/object_label)




## Inheritance

* **object_label** [ [denormalized_slot](denormalized_slot.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sssom:object_label |
| native | ontoassoc:object_label |




## LinkML Source

<details>
```yaml
name: object_label
description: The label of the ontology entity that is associated with the subject.
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- denormalized_slot
slot_uri: sssom:object_label
alias: object_label
domain_of:
- PositiveOrNegativeAssociation
range: string

```
</details>