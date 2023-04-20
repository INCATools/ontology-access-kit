# Slot: example_of_usage

URI: [IAO:0000112](http://purl.obolibrary.org/obo/IAO_0000112)




## Inheritance

* [informative_property](informative_property.md)
    * **example_of_usage**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasUserInformation](HasUserInformation.md) | 
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
name: example_of_usage
in_subset:
- allotrope permitted profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- skos:example
rank: 1000
is_a: informative_property
slot_uri: IAO:0000112
multivalued: true
alias: example_of_usage
domain_of:
- HasUserInformation
range: string

```
</details>