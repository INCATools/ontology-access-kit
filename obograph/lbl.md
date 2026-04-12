

# Slot: lbl


_the human-readable label of a node_





URI: [rdfs:label](http://www.w3.org/2000/01/rdf-schema#label)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SynonymTypeDefinition](SynonymTypeDefinition.md) |  |  no  |
| [Graph](Graph.md) | A graph is a collection of nodes and edges and other axioms that represents a... |  no  |
| [SubsetDefinition](SubsetDefinition.md) |  |  no  |
| [Node](Node.md) | A node is a class, property, or other entity in an ontology |  no  |







## Properties

* Range: [String](String.md)



## Aliases


* label
* name



## Comments

* the name "lbl" exists for legacy purposes, this should be considered identical to label in rdfs

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:label |
| native | obographs:lbl |




## LinkML Source

<details>
```yaml
name: lbl
description: the human-readable label of a node
comments:
- the name "lbl" exists for legacy purposes, this should be considered identical to
  label in rdfs
from_schema: https://github.com/geneontology/obographs
aliases:
- label
- name
rank: 1000
slot_uri: rdfs:label
alias: lbl
domain_of:
- Graph
- Node
- SubsetDefinition
- SynonymTypeDefinition
range: string

```
</details>