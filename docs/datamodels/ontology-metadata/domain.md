# Slot: domain

URI: [rdfs:domain](http://www.w3.org/2000/01/rdf-schema#domain)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **domain**





## Applicable Classes

| Name | Description |
| --- | --- |
[Property](Property.md) | 
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[Subset](Subset.md) | A collection of terms grouped for some purpose






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
name: domain
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
slot_uri: rdfs:domain
multivalued: true
alias: domain
domain_of:
- Property
range: string

```
</details>