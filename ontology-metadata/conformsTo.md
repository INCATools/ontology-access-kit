# Slot: conformsTo

URI: [dcterms:conformsTo](http://purl.org/dc/terms/conformsTo)




## Inheritance

* [informative_property](informative_property.md)
    * **conformsTo**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[HasCategory](HasCategory.md) |  |  no  |
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

* Range: [Thing](Thing.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: conformsTo
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: informative_property
slot_uri: dcterms:conformsTo
multivalued: true
alias: conformsTo
domain_of:
- HasCategory
range: Thing

```
</details>