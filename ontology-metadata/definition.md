# Slot: definition

URI: [IAO:0000115](http://purl.obolibrary.org/obo/IAO_0000115)




## Inheritance

* [core_property](core_property.md)
    * **definition**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[HasMinimalMetadata](HasMinimalMetadata.md) | Absolute minimum metadata model |  no  |
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
[Class](Class.md) |  |  yes  |
[Property](Property.md) |  |  yes  |
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
[HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
[Agent](Agent.md) |  |  no  |
[Image](Image.md) |  |  no  |
[Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |







## Properties

* Range: [NarrativeText](NarrativeText.md)

* Multivalued: True





## Comments

* SHOULD be in Aristotelian (genus-differentia) form

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: definition
comments:
- SHOULD be in Aristotelian (genus-differentia) form
in_subset:
- allotrope required profile
- go required profile
- obi required profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- skos:definition
rank: 1000
is_a: core_property
slot_uri: IAO:0000115
multivalued: true
alias: definition
domain_of:
- HasMinimalMetadata
range: narrative text

```
</details>