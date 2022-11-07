# Slot: definition_source

URI: [IAO:0000119](http://purl.obolibrary.org/obo/IAO_0000119)




## Inheritance

* [provenance_property](provenance_property.md)
    * **definition_source**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasProvenance](HasProvenance.md) | None
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | None
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
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
name: definition_source
todos:
- restrict range
in_subset:
- obi permitted profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: provenance_property
slot_uri: IAO:0000119
multivalued: true
alias: definition_source
domain_of:
- HasProvenance
range: string

```
</details>