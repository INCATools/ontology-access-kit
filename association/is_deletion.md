

# Slot: is_deletion



URI: [ontoassoc:is_deletion](https://w3id.org/oak/association/is_deletion)




## Inheritance

* **is_deletion** [ [diff_slot](diff_slot.md)]






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
| self | ontoassoc:is_deletion |
| native | ontoassoc:is_deletion |




## LinkML Source

<details>
```yaml
name: is_deletion
from_schema: https://w3id.org/oak/association
rank: 1000
mixins:
- diff_slot
alias: is_deletion
domain_of:
- AssociationChange
range: boolean

```
</details>