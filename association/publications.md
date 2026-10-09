

# Slot: publications


_The publications that support the association_





URI: [biolink:publications](https://w3id.org/biolink/vocab/publications)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |
| [AssociationChange](AssociationChange.md) | A change object describing a change between two associations |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | biolink:publications |
| native | ontoassoc:publications |




## LinkML Source

<details>
```yaml
name: publications
description: The publications that support the association
from_schema: https://w3id.org/oak/association
rank: 1000
slot_uri: biolink:publications
alias: publications
domain_of:
- PositiveOrNegativeAssociation
- AssociationChange
range: uriorcurie
multivalued: true

```
</details>