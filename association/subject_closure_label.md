# Slot: subject_closure_label


_The set of subjects that are related to the subject of the association via the closure predicates_



URI: [ontoassoc:subject_closure_label](https://w3id.org/oak/association/subject_closure_label)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
[Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |
[NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## LinkML Source

<details>
```yaml
name: subject_closure_label
description: The set of subjects that are related to the subject of the association
  via the closure predicates
from_schema: https://w3id.org/oak/association
rank: 1000
multivalued: true
alias: subject_closure_label
domain_of:
- PositiveOrNegativeAssociation
range: string

```
</details>