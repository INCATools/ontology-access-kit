

# Slot: classExpressions


_The set of class expressions that are mutually disjoint._





URI: [obographs:classExpressions](https://github.com/geneontology/obographs/classExpressions)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DisjointClassExpressionsAxiom](DisjointClassExpressionsAxiom.md) | An axiom that defines a set of classes or class expressions as being mutually... |  no  |







## Properties

* Range: [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md)

* Multivalued: True





## Comments

* currently restricted to existential restrictions (some values from)

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:classExpressions |
| native | obographs:classExpressions |




## LinkML Source

<details>
```yaml
name: classExpressions
description: The set of class expressions that are mutually disjoint.
comments:
- currently restricted to existential restrictions (some values from)
from_schema: https://github.com/geneontology/obographs
rank: 1000
alias: classExpressions
owner: DisjointClassExpressionsAxiom
domain_of:
- DisjointClassExpressionsAxiom
range: ExistentialRestrictionExpression
multivalued: true

```
</details>