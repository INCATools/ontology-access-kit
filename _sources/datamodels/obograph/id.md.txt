

# Slot: id


_The unique identifier of the entity_





URI: [obographs:id](https://github.com/geneontology/obographs/id)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Node](Node.md) | A node is a class, property, or other entity in an ontology |  no  |
| [SynonymTypeDefinition](SynonymTypeDefinition.md) |  |  no  |
| [SubsetDefinition](SubsetDefinition.md) |  |  no  |
| [Graph](Graph.md) | A graph is a collection of nodes and edges and other axioms that represents a... |  no  |







## Properties

* Range: [OboIdentifierString](OboIdentifierString.md)

* Required: True





## See Also

* [https://owlcollab.github.io/oboformat/doc/obo-syntax.html#2.5](https://owlcollab.github.io/oboformat/doc/obo-syntax.html#2.5)

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:id |
| native | obographs:id |




## LinkML Source

<details>
```yaml
name: id
description: The unique identifier of the entity
from_schema: https://github.com/geneontology/obographs
see_also:
- https://owlcollab.github.io/oboformat/doc/obo-syntax.html#2.5
rank: 1000
identifier: true
alias: id
domain_of:
- Graph
- Node
- SubsetDefinition
- SynonymTypeDefinition
range: OboIdentifierString
required: true

```
</details>