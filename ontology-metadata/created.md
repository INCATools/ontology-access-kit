# Slot: created
_when the term came into being_


URI: [dcterms:created](http://purl.org/dc/terms/created)




## Inheritance

* [provenance_property](provenance_property.md)
    * **created**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasProvenance](HasProvenance.md) | 
[Ontology](Ontology.md) | An OWL ontology
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

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: created
description: when the term came into being
from_schema: http://purl.obolibrary.org/obo/omo/schema
close_mappings:
- pav:createdOn
rank: 1000
is_a: provenance_property
slot_uri: dcterms:created
multivalued: false
alias: created
domain_of:
- HasProvenance
- Ontology
range: string

```
</details>