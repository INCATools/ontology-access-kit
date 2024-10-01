

# Slot: is_generalization


_True if the association was inferred to become more general (based on closure predicates). Note that depending on the tool, this may be inferred, if there is no explicit association-level migration information._





URI: [ontoassoc:is_generalization](https://w3id.org/oak/association/is_generalization)




## Inheritance

* **is_generalization** [ [diff_slot](diff_slot.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AssociationChange](AssociationChange.md) | A change object describing a change between two associations |  no  |







## Properties

* Range: [Boolean](Boolean.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:is_generalization |
| native | ontoassoc:is_generalization |




## LinkML Source

<details>
```yaml
name: is_generalization
description: True if the association was inferred to become more general (based on
  closure predicates). Note that depending on the tool, this may be inferred, if there
  is no explicit association-level migration information.
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- diff_slot
alias: is_generalization
domain_of:
- AssociationChange
range: boolean

```
</details>