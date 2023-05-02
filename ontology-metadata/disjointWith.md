# Slot: disjointWith

URI: [owl:disjointWith](http://www.w3.org/2002/07/owl#disjointWith)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **disjointWith**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ClassExpression](ClassExpression.md) |  |  no  |
[PropertyExpression](PropertyExpression.md) |  |  no  |
[Class](Class.md) |  |  no  |
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
[Restriction](Restriction.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: disjointWith
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
slot_uri: owl:disjointWith
multivalued: true
alias: disjointWith
domain_of:
- ClassExpression
- PropertyExpression
range: string

```
</details>