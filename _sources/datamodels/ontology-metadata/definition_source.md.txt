# Slot: definition_source

URI: [IAO:0000119](http://purl.obolibrary.org/obo/IAO_0000119)




## Inheritance

* [provenance_property](provenance_property.md)
    * **definition_source**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasProvenance](HasProvenance.md) | 
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | 
[Property](Property.md) | 
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[HomoSapiens](HomoSapiens.md) | An individual human being
[Agent](Agent.md) | 
[Image](Image.md) | 
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