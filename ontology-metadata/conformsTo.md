# Slot: conformsTo

URI: [dcterms:conformsTo](http://purl.org/dc/terms/conformsTo)




## Inheritance

* [informative_property](informative_property.md)
    * **conformsTo**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasCategory](HasCategory.md) | None
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | None
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[Subset](Subset.md) | A collection of terms grouped for some purpose






## Properties

* Range: [Thing](Thing.md)
* Multivalued: True







## Alias




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