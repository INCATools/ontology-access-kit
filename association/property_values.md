

# Slot: property_values


_Arbitrary key-value pairs with additional information about the association_



URI: [ontoassoc:property_values](https://w3id.org/oak/association/property_values)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [NegatedAssociation](NegatedAssociation.md) | A negated association between a thing (subject) and another thing (object) |  no  |
| [PositiveOrNegativeAssociation](PositiveOrNegativeAssociation.md) |  |  no  |
| [Association](Association.md) | A generic association between a thing (subject) and another thing (object) |  no  |







## Properties

* Range: [PropertyValue](PropertyValue.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## LinkML Source

<details>
```yaml
name: property_values
description: Arbitrary key-value pairs with additional information about the association
from_schema: https://w3id.org/oak/association
rank: 1000
multivalued: true
alias: property_values
domain_of:
- PositiveOrNegativeAssociation
range: PropertyValue
inlined: true

```
</details>