

# Slot: pipelines


_all pipelines used to build the index_





URI: [mappingrules:pipelines](https://w3id.org/oak/mapping-rules-datamodel/pipelines)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [LexicalIndex](LexicalIndex.md) | An index over an ontology keyed by lexical unit |  no  |







## Properties

* Range: [LexicalTransformationPipeline](LexicalTransformationPipeline.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:pipelines |
| native | mappingrules:pipelines |




## LinkML Source

<details>
```yaml
name: pipelines
description: all pipelines used to build the index
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
alias: pipelines
owner: LexicalIndex
domain_of:
- LexicalIndex
range: LexicalTransformationPipeline
multivalued: true
inlined: true

```
</details>