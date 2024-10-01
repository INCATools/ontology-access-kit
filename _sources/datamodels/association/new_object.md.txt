

# Slot: new_object


_The object (e.g. term) on the new association_





URI: [ontoassoc:new_object](https://w3id.org/oak/association/new_object)




## Inheritance

* [object](object.md)
    * **new_object** [ [diff_slot](diff_slot.md)]






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
| self | ontoassoc:new_object |
| native | ontoassoc:new_object |




## LinkML Source

<details>
```yaml
name: new_object
description: The object (e.g. term) on the new association
from_schema: https://w3id.org/oak/association
rank: 1000
is_a: object
mixins:
- diff_slot
alias: new_object
domain_of:
- AssociationChange
range: uriorcurie

```
</details>