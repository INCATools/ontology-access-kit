# Slot: type

URI: [rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **type**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[Thing](Thing.md) |  |  no  |
[NamedObject](NamedObject.md) | Anything with an IRI |  no  |
[Ontology](Ontology.md) | An OWL ontology |  no  |
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
[Class](Class.md) |  |  no  |
[Property](Property.md) |  |  no  |
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
[HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
[Agent](Agent.md) |  |  no  |
[Image](Image.md) |  |  no  |
[Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

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