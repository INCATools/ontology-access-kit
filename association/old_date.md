

# Slot: old_date


_The date of the old association_



URI: [ontoassoc:old_date](https://w3id.org/oak/association/old_date)




## Inheritance

* [date](date.md)
    * **old_date** [ [diff_slot](diff_slot.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AssociationChange](AssociationChange.md) | A change object describing a change between two associations |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## LinkML Source

<details>
```yaml
name: old_date
description: The date of the old association
from_schema: https://w3id.org/oak/association
rank: 1000
is_a: date
mixins:
- diff_slot
alias: old_date
domain_of:
- AssociationChange
range: string

```
</details>