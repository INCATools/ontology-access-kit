# Slot: pred
_the predicate of an edge_


URI: [rdf:predicate](http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[Edge](Edge.md) | An edge is a typed relationship between two nodes
[SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity
[PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec...
[DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of...
[BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d...
[XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to ...






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)







## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## LinkML Source

<details>
```yaml
name: pred
description: the predicate of an edge
from_schema: https://github.com/geneontology/obographs
rank: 1000
slot_uri: rdf:predicate
alias: pred
domain_of:
- Edge
- SynonymPropertyValue
- PropertyValue
range: string

```
</details>