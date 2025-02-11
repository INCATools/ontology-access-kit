

# Slot: sub


_the subject of an edge_





URI: [rdf:subject](http://www.w3.org/1999/02/22-rdf-syntax-ns#subject)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Edge](Edge.md) | An edge is a simple typed relationship between two nodes |  yes  |







## Properties

* Range: [String](String.md)



## Aliases


* subject
* source
* child
* head



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:subject |
| native | obographs:sub |




## LinkML Source

<details>
```yaml
name: sub
description: the subject of an edge
from_schema: https://github.com/geneontology/obographs
aliases:
- subject
- source
- child
- head
rank: 1000
slot_uri: rdf:subject
alias: sub
domain_of:
- Edge
range: string

```
</details>