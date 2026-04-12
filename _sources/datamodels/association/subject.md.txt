

# Slot: subject


_The thing which the association is about._





URI: [rdf:subject](rdf:subject)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AssociationChange](AssociationChange.md) | A change object describing a change between two associations |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
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
| self | rdf:subject |
| native | ontoassoc:subject |
| exact | oa:hasBody |




## LinkML Source

<details>
```yaml
name: subject
description: The thing which the association is about.
comments:
- it is conventional for the subject to be the "entity" and the object to be the ontological
  descriptor
from_schema: https://w3id.org/oak/association
exact_mappings:
- oa:hasBody
rank: 1000
slot_uri: rdf:subject
alias: subject
domain_of:
- PositiveOrNegativeAssociation
- AssociationChange
slot_group: core_triple
range: uriorcurie

```
</details>