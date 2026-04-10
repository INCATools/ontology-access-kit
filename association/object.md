

# Slot: object


_An ontology entity that is associated with the subject._





URI: [rdf:object](rdf:object)




## Inheritance

* **object**
    * [old_object](old_object.md) [ [diff_slot](diff_slot.md)]
    * [new_object](new_object.md) [ [diff_slot](diff_slot.md)]
    * [object1](object1.md)
    * [object2](object2.md)






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)





## Comments

* it is conventional for the subject to be the "entity" and the object to be the ontological descriptor

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:object |
| native | ontoassoc:object |
| exact | oa:hasTarget |




## LinkML Source

<details>
```yaml
name: object
description: An ontology entity that is associated with the subject.
comments:
- it is conventional for the subject to be the "entity" and the object to be the ontological
  descriptor
from_schema: https://w3id.org/oak/association
exact_mappings:
- oa:hasTarget
rank: 1000
slot_uri: rdf:object
alias: object
domain_of:
- PositiveOrNegativeAssociation
slot_group: core_triple
range: uriorcurie

```
</details>