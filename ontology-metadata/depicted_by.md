# Slot: depicted_by

URI: [foaf:depicted_by](http://xmlns.com/foaf/0.1/depicted_by)




## Inheritance

* [informative_property](informative_property.md)
    * **depicted_by**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[HasUserInformation](HasUserInformation.md) |  |  no  |
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

* Range: [Image](Image.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: depicted_by
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: informative_property
slot_uri: foaf:depicted_by
multivalued: true
alias: depicted_by
domain_of:
- HasUserInformation
range: Image

```
</details>