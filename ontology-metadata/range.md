# Slot: range

URI: [rdfs:range](http://www.w3.org/2000/01/rdf-schema#range)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **range**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Property](Property.md) |  |  no  |
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
[Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |







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
name: range
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
slot_uri: rdfs:range
multivalued: true
alias: range
domain_of:
- Property
range: string

```
</details>