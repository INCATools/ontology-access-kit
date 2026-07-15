

# Slot: val


_the value of a property_





URI: [rdf:object](http://www.w3.org/1999/02/22-rdf-syntax-ns#object)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to ... |  yes  |
| [SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity |  yes  |
| [DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of... |  yes  |
| [BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d... |  no  |
| [PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec... |  no  |







## Properties

* Range: [String](String.md)



## Aliases


* value



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:object |
| native | obographs:val |




## LinkML Source

<details>
```yaml
name: val
description: the value of a property
from_schema: https://github.com/geneontology/obographs
aliases:
- value
rank: 1000
slot_uri: rdf:object
alias: val
domain_of:
- PropertyValue
range: string

```
</details>