

# Slot: subject_closure


_The set of subjects that are related to the subject of the association via the closure predicates_





URI: [ontoassoc:subject_closure](https://w3id.org/oak/association/subject_closure)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
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
| self | ontoassoc:subject_closure |
| native | ontoassoc:subject_closure |




## LinkML Source

<details>
```yaml
name: subject_closure
description: The set of subjects that are related to the subject of the association
  via the closure predicates
from_schema: https://w3id.org/oak/association
rank: 1000
alias: subject_closure
domain_of:
- PositiveOrNegativeAssociation
range: uriorcurie
multivalued: true

```
</details>