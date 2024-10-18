

# Slot: disjointWith



URI: [owl:disjointWith](http://www.w3.org/2002/07/owl#disjointWith)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **disjointWith**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PropertyExpression](PropertyExpression.md) |  |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [ClassExpression](ClassExpression.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [Restriction](Restriction.md) |  |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |







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
| self | owl:disjointWith |
| native | omoschema:disjointWith |




## LinkML Source

<details>
```yaml
name: disjointWith
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: logical_predicate
slot_uri: owl:disjointWith
alias: disjointWith
domain_of:
- ClassExpression
- PropertyExpression
range: string
multivalued: true

```
</details>