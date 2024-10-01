

# Slot: preconditions


_all of the criteria that must be true before a rule is fired_





URI: [sh:condition](https://w3id.org/shacl/condition)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MappingRule](MappingRule.md) | An individual mapping rule, if preconditions match the postconditions are app... |  no  |







## Properties

* Range: [Precondition](Precondition.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:condition |
| native | mappingrules:preconditions |




## LinkML Source

<details>
```yaml
name: preconditions
description: all of the criteria that must be true before a rule is fired
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
slot_uri: sh:condition
alias: preconditions
owner: MappingRule
domain_of:
- MappingRule
range: Precondition

```
</details>