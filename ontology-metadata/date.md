# Slot: date
_when the term was updated_


URI: [dcterms:date](http://purl.org/dc/terms/date)




## Inheritance

* [provenance_property](provenance_property.md)
    * **date**





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








## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: date
description: when the term was updated
from_schema: http://purl.obolibrary.org/obo/omo/schema
close_mappings:
- pav:authoredOn
rank: 1000
is_a: provenance_property
slot_uri: dcterms:date
multivalued: true
alias: date
domain_of:
- HasProvenance
range: string

```
</details>