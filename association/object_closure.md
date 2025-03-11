

# Slot: object_closure


_The set of objects that are related to the object of the association via the closure predicates_





URI: [ontoassoc:object_closure](https://w3id.org/oak/association/object_closure)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:object_closure |
| native | ontoassoc:object_closure |




## LinkML Source

<details>
```yaml
name: object_closure
description: The set of objects that are related to the object of the association
  via the closure predicates
from_schema: https://w3id.org/oak/association
rank: 1000
alias: object_closure
domain_of:
- PositiveOrNegativeAssociation
range: uriorcurie
multivalued: true

```
</details>