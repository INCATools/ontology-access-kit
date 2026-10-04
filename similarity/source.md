

# Slot: source


_The system or resource that computed the scores, e.g. oaklib, ubergraph_





URI: [sim:source](https://w3id.org/linkml/similarity/source)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [InformationContentMethod](InformationContentMethod.md) | Describes how information content (IC) scores were computed |  no  |







## Properties

* Range: [String](String.md)






## Examples

| Value |
| --- |
| ubergraph |

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:source |
| native | sim:source |




## LinkML Source

<details>
```yaml
name: source
description: The system or resource that computed the scores, e.g. oaklib, ubergraph
examples:
- value: ubergraph
from_schema: https://w3id.org/oak/similarity
rank: 1000
alias: source
owner: InformationContentMethod
domain_of:
- InformationContentMethod
range: string

```
</details>