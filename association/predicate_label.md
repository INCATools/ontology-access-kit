

# Slot: predicate_label


_The label of the type of relationship between the subject and object._





URI: [sssom:predicate_label](https://w3id.org/sssom/predicate_label)




## Inheritance

* **predicate_label** [ [denormalized_slot](denormalized_slot.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sssom:predicate_label |
| native | ontoassoc:predicate_label |




## LinkML Source

<details>
```yaml
name: predicate_label
description: The label of the type of relationship between the subject and object.
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- denormalized_slot
slot_uri: sssom:predicate_label
alias: predicate_label
domain_of:
- PositiveOrNegativeAssociation
range: string

```
</details>