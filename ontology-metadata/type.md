# Slot: type

URI: [rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **type**





## Applicable Classes

| Name | Description |
| --- | --- |
[Thing](Thing.md) | 
[NamedObject](NamedObject.md) | Anything with an IRI
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

* Range: [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)
* Multivalued: True








## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: type
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
slot_uri: rdf:type
multivalued: true
designates_type: true
alias: type
domain_of:
- Thing
range: uriorcurie

```
</details>