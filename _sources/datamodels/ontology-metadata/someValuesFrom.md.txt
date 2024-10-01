

# Slot: someValuesFrom



URI: [owl:someValuesFrom](http://www.w3.org/2002/07/owl#someValuesFrom)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **someValuesFrom**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Restriction](Restriction.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:someValuesFrom |
| native | omoschema:someValuesFrom |




## LinkML Source

<details>
```yaml
name: someValuesFrom
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: logical_predicate
slot_uri: owl:someValuesFrom
alias: someValuesFrom
domain_of:
- Restriction
range: string
multivalued: true

```
</details>