

# Slot: new_date


_The date of the new association_





URI: [ontoassoc:new_date](https://w3id.org/oak/association/new_date)




## Inheritance

* [date](date.md)
    * **new_date** [ [diff_slot](diff_slot.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AssociationChange](AssociationChange.md) | A change object describing a change between two associations |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:new_date |
| native | ontoassoc:new_date |




## LinkML Source

<details>
```yaml
name: new_date
description: The date of the new association
from_schema: https://w3id.org/oak/association
rank: 1000
is_a: date
mixins:
- diff_slot
alias: new_date
domain_of:
- AssociationChange
range: string

```
</details>