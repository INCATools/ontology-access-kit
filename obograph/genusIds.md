

# Slot: genusIds


_The set of classes that are the genus of the defined class_





URI: [obographs:genusIds](https://github.com/geneontology/obographs/genusIds)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | An axiom that defines a class in terms of a genus or set of genus classes and... |  no  |







## Properties

* Range: [OboIdentifierString](OboIdentifierString.md)

* Multivalued: True

* Recommended: True





## Comments

* typically, this will be a single class

## See Also

* [https://github.com/geneontology/obographs/issues/89](https://github.com/geneontology/obographs/issues/89)

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:genusIds |
| native | obographs:genusIds |




## LinkML Source

<details>
```yaml
name: genusIds
description: The set of classes that are the genus of the defined class
comments:
- typically, this will be a single class
from_schema: https://github.com/geneontology/obographs
see_also:
- https://github.com/geneontology/obographs/issues/89
rank: 1000
alias: genusIds
owner: LogicalDefinitionAxiom
domain_of:
- LogicalDefinitionAxiom
range: OboIdentifierString
recommended: true
multivalued: true

```
</details>