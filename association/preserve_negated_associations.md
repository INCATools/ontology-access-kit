

# Slot: preserve_negated_associations


_If true, then the parser will keep negated associations in the output._

_If false, then the parser will remove negated associations from the output._





URI: [ontoassoc:preserve_negated_associations](https://w3id.org/oak/association/preserve_negated_associations)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ParserConfiguration](ParserConfiguration.md) | Settings that determine behavior when parsing associations |  no  |







## Properties

* Range: [Boolean](Boolean.md)





## Comments

* Note that to be defensive most applications should leave the default as false

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/association




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontoassoc:preserve_negated_associations |
| native | ontoassoc:preserve_negated_associations |




## LinkML Source

<details>
```yaml
name: preserve_negated_associations
description: 'If true, then the parser will keep negated associations in the output.

  If false, then the parser will remove negated associations from the output.'
comments:
- Note that to be defensive most applications should leave the default as false
from_schema: https://w3id.org/oak/association
rank: 1000
alias: preserve_negated_associations
owner: ParserConfiguration
domain_of:
- ParserConfiguration
range: boolean

```
</details>