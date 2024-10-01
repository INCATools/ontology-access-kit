

# Slot: term


_A normalized term that groups ontology elements_





URI: [mappingrules:term](https://w3id.org/oak/mapping-rules-datamodel/term)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [LexicalGrouping](LexicalGrouping.md) | A grouping of ontology elements by a shared lexical term |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:term |
| native | mappingrules:term |




## LinkML Source

<details>
```yaml
name: term
description: A normalized term that groups ontology elements
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
key: true
alias: term
owner: LexicalGrouping
domain_of:
- LexicalGrouping
range: string
required: true

```
</details>