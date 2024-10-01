

# Slot: is_specialization


_True if the association was inferred to become more specific (based on closure predicates). Note that depending on the tool, this may be inferred, if there is no explicit association-level migration information._





URI: [ontoassoc:is_specialization](https://w3id.org/oak/association/is_specialization)




## Inheritance

* **is_specialization** [ [diff_slot](diff_slot.md)]






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
| self | ontoassoc:is_specialization |
| native | ontoassoc:is_specialization |




## LinkML Source

<details>
```yaml
name: is_specialization
description: True if the association was inferred to become more specific (based on
  closure predicates). Note that depending on the tool, this may be inferred, if there
  is no explicit association-level migration information.
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- diff_slot
alias: is_specialization
domain_of:
- AssociationChange
range: boolean

```
</details>