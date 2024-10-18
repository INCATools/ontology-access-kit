

# Slot: valType


_the datatype of a property value_





URI: [obographs:valType](https://github.com/geneontology/obographs/valType)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [XrefPropertyValue](XrefPropertyValue.md) | A property value that represents an assertion about an external reference to ... |  no  |
| [BasicPropertyValue](BasicPropertyValue.md) | A property value that represents an assertion about an entity that is not a d... |  no  |
| [SynonymPropertyValue](SynonymPropertyValue.md) | A property value that represents an assertion about a synonym of an entity |  no  |
| [DefinitionPropertyValue](DefinitionPropertyValue.md) | A property value that represents an assertion about the textual definition of... |  no  |
| [PropertyValue](PropertyValue.md) | A generic grouping for the different kinds of key-value associations on objec... |  no  |







## Properties

* Range: [String](String.md)



## Aliases


* value type
* datatype



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:valType |
| native | obographs:valType |




## LinkML Source

<details>
```yaml
name: valType
description: the datatype of a property value
from_schema: https://github.com/geneontology/obographs
aliases:
- value type
- datatype
rank: 1000
alias: valType
domain_of:
- PropertyValue
range: string

```
</details>