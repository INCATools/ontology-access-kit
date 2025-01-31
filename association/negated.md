

# Slot: negated


_True if the association is negated - i.e the core triple is not true._





URI: [ontoassoc:negated](https://w3id.org/oak/association/negated)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  yes  |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  yes  |







## Properties

* Range: [Boolean](Boolean.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:negated |
| native | ontoassoc:negated |




## LinkML Source

<details>
```yaml
name: negated
description: True if the association is negated - i.e the core triple is not true.
from_schema: https://w3id.org/oak/association
rank: 1000
alias: negated
domain_of:
- PositiveOrNegativeAssociation
range: boolean

```
</details>