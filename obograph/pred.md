

# Slot: pred


_the predicate of an edge_





URI: [rdf:predicate](http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Edge](Edge.md) | An edge is a simple typed relationship between two nodes |  yes  |
| [XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to ... |  no  |
| [PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec... |  no  |
| [SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity |  yes  |
| [DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of... |  no  |
| [SynonymTypeDefinition](SynonymTypeDefinition.md) |  |  no  |
| [BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d... |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:predicate |
| native | obographs:pred |




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
- SynonymTypeDefinition
range: string

```
</details>