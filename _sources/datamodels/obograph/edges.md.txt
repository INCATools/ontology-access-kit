# Slot: edges
_All edges present in a graph._


URI: [og:edges](https://github.com/geneontology/obographs/edges)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[Graph](Graph.md) | A graph is a collection of nodes and edges that represents a single ontology






## Properties

* Range: [Edge](Edge.md)
* Multivalued: True








## Comments

* Note that this only includes core edges, formed by translating (a) SubClassOf between named classes (b) SubPropertyOf (c) SubClassOf between a named class and a simple existential axiom (d) ObjectPropertyAssertions

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## LinkML Source

<details>
```yaml
name: edges
description: All edges present in a graph.
comments:
- Note that this only includes core edges, formed by translating (a) SubClassOf between
  named classes (b) SubPropertyOf (c) SubClassOf between a named class and a simple
  existential axiom (d) ObjectPropertyAssertions
from_schema: https://github.com/geneontology/obographs
rank: 1000
multivalued: true
alias: edges
domain_of:
- Graph
range: Edge
inlined: true
inlined_as_list: true

```
</details>