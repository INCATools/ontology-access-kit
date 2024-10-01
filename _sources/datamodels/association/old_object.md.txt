

# Slot: old_object


_The object (e.g. term) on the old association_





URI: [ontoassoc:old_object](https://w3id.org/oak/association/old_object)




## Inheritance

* [object](object.md)
    * **old_object** [ [diff_slot](diff_slot.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AssociationChange](AssociationChange.md) | A change object describing a change between two associations |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:old_object |
| native | ontoassoc:old_object |




## LinkML Source

<details>
```yaml
name: old_object
description: The object (e.g. term) on the old association
from_schema: https://w3id.org/oak/association
rank: 1000
is_a: object
mixins:
- diff_slot
alias: old_object
domain_of:
- AssociationChange
range: uriorcurie

```
</details>