# Slot: category

URI: [biolink:category](https://w3id.org/biolink/vocab/category)




## Inheritance

* [informative_property](informative_property.md)
    * **category**





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

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: category
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: informative_property
slot_uri: biolink:category
alias: category
domain_of:
- HasCategory
range: string

```
</details>