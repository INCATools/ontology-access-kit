

# Slot: predicate


_The type of relationship between the subject and object._





URI: [rdf:predicate](rdf:predicate)




## Inheritance

* **predicate**
    * [old_predicate](old_predicate.md) [ [diff_slot](diff_slot.md)]
    * [new_predicate](new_predicate.md) [ [diff_slot](diff_slot.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [PropertyValue](PropertyValue.md) | A generic tag-value that can be associated with an association |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:predicate |
| native | ontoassoc:predicate |




## LinkML Source

<details>
```yaml
name: predicate
description: The type of relationship between the subject and object.
from_schema: https://w3id.org/oak/association
rank: 1000
slot_uri: rdf:predicate
alias: predicate
domain_of:
- PositiveOrNegativeAssociation
- PropertyValue
slot_group: core_triple
range: uriorcurie

```
</details>