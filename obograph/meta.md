# Slot: meta
_A collection of metadata about either an ontology (graph), an entity, or an axiom_


URI: [og:meta](https://github.com/geneontology/obographs/meta)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[GraphDocument](GraphDocument.md) | A graph document is a collection of graphs together with a set of prefixes th...
[Graph](Graph.md) | A graph is a collection of nodes and edges that represents a single ontology
[Node](Node.md) | A node is a class, property, or other entity in an ontology
[Edge](Edge.md) | An edge is a typed relationship between two nodes
[PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec...
[Axiom](Axiom.md) | A generic grouping for any OWL axiom that is not captured by existing constru...
[DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of...
[BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d...
[XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to ...
[SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity
[DomainRangeAxiom](DomainRangeAxiom.md) | An axiom that represents some combination of domain and range assertions
[EquivalentNodesSet](EquivalentNodesSet.md) | A clique of nodes that are all mutually equivalent
[LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | An axiom that defines a class in terms of a genus or set of genus classes and...
[PropertyChainAxiom](PropertyChainAxiom.md) | An axiom that represents an OWL property chain, e






## Properties

* Range: [Meta](Meta.md)





## Aliases


* annotations



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## LinkML Source

<details>
```yaml
name: meta
description: A collection of metadata about either an ontology (graph), an entity,
  or an axiom
from_schema: https://github.com/geneontology/obographs
aliases:
- annotations
rank: 1000
alias: meta
domain_of:
- GraphDocument
- Graph
- Node
- Edge
- PropertyValue
- Axiom
range: Meta

```
</details>