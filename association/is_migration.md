

# Slot: is_migration


_if the object (e.g. term) of the old object has been obsoleted, and the object has been migrated (either automatically or manually) to a new object based on obsoletion migration metadata, this is True_





URI: [ontoassoc:is_migration](https://w3id.org/oak/association/is_migration)




## Inheritance

* **is_migration** [ [diff_slot](diff_slot.md)]






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
| self | ontoassoc:is_migration |
| native | ontoassoc:is_migration |




## LinkML Source

<details>
```yaml
name: is_migration
description: if the object (e.g. term) of the old object has been obsoleted, and the
  object has been migrated (either automatically or manually) to a new object based
  on obsoletion migration metadata, this is True
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- diff_slot
alias: is_migration
domain_of:
- AssociationChange
range: boolean

```
</details>