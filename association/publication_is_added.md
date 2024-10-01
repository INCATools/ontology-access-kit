

# Slot: publication_is_added


_True if the publication was not present in the old association set (and present in the new)_





URI: [ontoassoc:publication_is_added](https://w3id.org/oak/association/publication_is_added)




## Inheritance

* **publication_is_added** [ [diff_slot](diff_slot.md)]






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
| self | ontoassoc:publication_is_added |
| native | ontoassoc:publication_is_added |




## LinkML Source

<details>
```yaml
name: publication_is_added
description: True if the publication was not present in the old association set (and
  present in the new)
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- diff_slot
alias: publication_is_added
domain_of:
- AssociationChange
range: boolean

```
</details>