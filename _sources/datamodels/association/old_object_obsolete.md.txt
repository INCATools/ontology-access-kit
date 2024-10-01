

# Slot: old_object_obsolete


_if the object (e.g. term) of the old object has been obsoleted, this is true_





URI: [ontoassoc:old_object_obsolete](https://w3id.org/oak/association/old_object_obsolete)




## Inheritance

* **old_object_obsolete** [ [diff_slot](diff_slot.md)]






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
| self | ontoassoc:old_object_obsolete |
| native | ontoassoc:old_object_obsolete |




## LinkML Source

<details>
```yaml
name: old_object_obsolete
description: if the object (e.g. term) of the old object has been obsoleted, this
  is true
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- diff_slot
alias: old_object_obsolete
domain_of:
- AssociationChange
range: boolean

```
</details>