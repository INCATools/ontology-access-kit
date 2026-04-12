

# Slot: complementOf



URI: [owl:complementOf](http://www.w3.org/2002/07/owl#complementOf)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **complementOf**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Class](Class.md) |  |  no  |
| [Restriction](Restriction.md) |  |  no  |
| [ClassExpression](ClassExpression.md) |  |  no  |







## Properties

* Range: [String](String.md)





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:complementOf |
| native | omoschema:complementOf |




## LinkML Source

<details>
```yaml
name: complementOf
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: logical_predicate
slot_uri: owl:complementOf
alias: complementOf
domain_of:
- ClassExpression
range: string

```
</details>