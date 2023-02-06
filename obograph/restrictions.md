# Slot: restrictions
_The set of restrictions that are the differentia of the defined class_


URI: [owl:someValuesFrom](http://www.w3.org/2002/07/owl#someValuesFrom)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | An axiom that defines a class in terms of a genus or set of genus classes and...






## Properties

* Range: [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md)
* Multivalued: True

* Recommended: True






## Aliases


* differentia



## Comments

* typically this will always be present.

## See Also

* [https://github.com/geneontology/obographs/issues/89](https://github.com/geneontology/obographs/issues/89)

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## LinkML Source

<details>
```yaml
name: restrictions
description: The set of restrictions that are the differentia of the defined class
comments:
- typically this will always be present.
from_schema: https://github.com/geneontology/obographs
see_also:
- https://github.com/geneontology/obographs/issues/89
aliases:
- differentia
rank: 1000
slot_uri: owl:someValuesFrom
multivalued: true
alias: restrictions
owner: LogicalDefinitionAxiom
domain_of:
- LogicalDefinitionAxiom
range: ExistentialRestrictionExpression
recommended: true

```
</details>