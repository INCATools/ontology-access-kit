

# Slot: comments


_Comments about the association_





URI: [rdfs:comment](rdfs:comment)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:comment |
| native | ontoassoc:comments |




## LinkML Source

<details>
```yaml
name: comments
description: Comments about the association
from_schema: https://w3id.org/oak/association
rank: 1000
slot_uri: rdfs:comment
alias: comments
domain_of:
- PositiveOrNegativeAssociation
range: string
multivalued: true

```
</details>