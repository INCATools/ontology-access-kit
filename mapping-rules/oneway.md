

# Slot: oneway


_if true then subject and object can be switched and predicate inverted_





URI: [mappingrules:oneway](https://w3id.org/oak/mapping-rules-datamodel/oneway)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MappingRule](MappingRule.md) | An individual mapping rule, if preconditions match the postconditions are app... |  no  |







## Properties

* Range: [Boolean](Boolean.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:oneway |
| native | mappingrules:oneway |




## LinkML Source

<details>
```yaml
name: oneway
description: if true then subject and object can be switched and predicate inverted
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
ifabsent: 'False'
alias: oneway
owner: MappingRule
domain_of:
- MappingRule
range: boolean

```
</details>