

# Slot: edges


_All edges present in a graph._





URI: [obographs:edges](https://github.com/geneontology/obographs/edges)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Graph](Graph.md) | A graph is a collection of nodes and edges and other axioms that represents a... |  no  |







## Properties

* Range: [Edge](Edge.md)

* Multivalued: True





## Comments

* Note that this only includes core edges, formed by translating (a) SubClassOf between named classes (b) SubPropertyOf (c) SubClassOf between a named class and a simple existential axiom (d) ObjectPropertyAssertions

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:edges |
| native | obographs:edges |




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
alias: edges
domain_of:
- Graph
range: Edge
multivalued: true
inlined: true
inlined_as_list: true

```
</details>