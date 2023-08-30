# Slot: meta


_A collection of metadata about either an ontology (graph), an entity, or an axiom_



URI: [obographs:meta](https://github.com/geneontology/obographs/meta)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[GraphDocument](GraphDocument.md) | A graph document is a collection of graphs together with a set of prefixes th... |  no  |
[Graph](Graph.md) | A graph is a collection of nodes and edges and other axioms that represents a... |  no  |
[Node](Node.md) | A node is a class, property, or other entity in an ontology |  no  |
[Edge](Edge.md) | An edge is a simple typed relationship between two nodes |  no  |
[PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec... |  no  |
[Axiom](Axiom.md) | A generic grouping for any OWL axiom or group of axioms that is not captured ... |  no  |
[DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of... |  no  |
[BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d... |  no  |
[XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to ... |  no  |
[SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity |  no  |
[DomainRangeAxiom](DomainRangeAxiom.md) | This groups potentially multiple axioms that constrain the usage of a propert... |  no  |
[EquivalentNodesSet](EquivalentNodesSet.md) | A clique of nodes that are all mutually equivalent |  no  |
[LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | An axiom that defines a class in terms of a genus or set of genus classes and... |  no  |
[DisjointClassExpressionsAxiom](DisjointClassExpressionsAxiom.md) | An axiom that defines a set of classes or class expressions as being mutually... |  no  |
[PropertyChainAxiom](PropertyChainAxiom.md) | An axiom that represents an OWL property chain, e |  no  |







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