

# Slot: publication_is_deleted


_True if the publication is not present in the new association set (and present in the old)_





URI: [ontoassoc:publication_is_deleted](https://w3id.org/oak/association/publication_is_deleted)




## Inheritance

* **publication_is_deleted** [ [diff_slot](diff_slot.md)]






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
| self | ontoassoc:publication_is_deleted |
| native | ontoassoc:publication_is_deleted |




## LinkML Source

<details>
```yaml
name: publication_is_deleted
description: True if the publication is not present in the new association set (and
  present in the old)
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- diff_slot
alias: publication_is_deleted
domain_of:
- AssociationChange
range: boolean

```
</details>