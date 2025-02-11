

# Slot: obj


_the object of an edge_





URI: [rdf:object](http://www.w3.org/1999/02/22-rdf-syntax-ns#object)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Edge](Edge.md) | An edge is a simple typed relationship between two nodes |  yes  |







## Properties

* Range: [String](String.md)



## Aliases


* object
* target
* parent
* tail



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:object |
| native | obographs:obj |




## LinkML Source

<details>
```yaml
name: obj
description: the object of an edge
from_schema: https://github.com/geneontology/obographs
aliases:
- object
- target
- parent
- tail
rank: 1000
slot_uri: rdf:object
alias: obj
domain_of:
- Edge
range: string

```
</details>