

# Slot: is_creation



URI: [ontoassoc:is_creation](https://w3id.org/oak/association/is_creation)




## Inheritance

* **is_creation** [ [diff_slot](diff_slot.md)]






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
| self | ontoassoc:is_creation |
| native | ontoassoc:is_creation |




## LinkML Source

<details>
```yaml
name: is_creation
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- diff_slot
alias: is_creation
domain_of:
- AssociationChange
range: boolean

```
</details>