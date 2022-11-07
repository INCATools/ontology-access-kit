# Slot: id
_this maps to the URI in RDF_


URI: [omoschema:id](http://purl.obolibrary.org/obo/schema/id)




## Inheritance

* [core_property](core_property.md)
    * **id**





## Applicable Classes

| Name | Description |
| --- | --- |
[NamedObject](NamedObject.md) | Anything with an IRI
[Ontology](Ontology.md) | An OWL ontology
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | None
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[Subset](Subset.md) | A collection of terms grouped for some purpose






## Properties

* Range: [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)
* Required: True







## Alias




## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: id
description: this maps to the URI in RDF
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: core_property
identifier: true
alias: id
domain_of:
- NamedObject
range: uriorcurie
required: true

```
</details>