# Slot: range

URI: [rdfs:range](http://www.w3.org/2000/01/rdf-schema#range)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **range**





## Applicable Classes

| Name | Description |
| --- | --- |
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[Subset](Subset.md) | A collection of terms grouped for some purpose






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## Alias




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