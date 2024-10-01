

# Slot: new_predicate


_If the association diff is a change in predicate, this is the predicate on the new association_





URI: [ontoassoc:new_predicate](https://w3id.org/oak/association/new_predicate)




## Inheritance

* [predicate](predicate.md)
    * **new_predicate** [ [diff_slot](diff_slot.md)]






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
| self | ontoassoc:new_predicate |
| native | ontoassoc:new_predicate |




## LinkML Source

<details>
```yaml
name: new_predicate
description: If the association diff is a change in predicate, this is the predicate
  on the new association
from_schema: https://w3id.org/oak/association
rank: 1000
is_a: predicate
mixins:
- diff_slot
alias: new_predicate
domain_of:
- AssociationChange
range: uriorcurie

```
</details>