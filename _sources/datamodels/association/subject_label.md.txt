

# Slot: subject_label


_The label of the thing which the association is about._





URI: [sssom:subject_label](https://w3id.org/sssom/subject_label)




## Inheritance

* **subject_label** [ [denormalized_slot](denormalized_slot.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sssom:subject_label |
| native | ontoassoc:subject_label |




## LinkML Source

<details>
```yaml
name: subject_label
description: The label of the thing which the association is about.
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- denormalized_slot
slot_uri: sssom:subject_label
alias: subject_label
domain_of:
- PositiveOrNegativeAssociation
range: string

```
</details>