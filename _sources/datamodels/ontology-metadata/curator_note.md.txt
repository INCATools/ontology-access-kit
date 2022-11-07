# Slot: curator_note

URI: [IAO:0000232](http://purl.obolibrary.org/obo/IAO_0000232)




## Inheritance

* [provenance_property](provenance_property.md)
    * **curator_note**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasUserInformation](HasUserInformation.md) | None
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




## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: curator_note
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: provenance_property
slot_uri: IAO:0000232
multivalued: true
alias: curator_note
domain_of:
- HasUserInformation
range: string

```
</details>