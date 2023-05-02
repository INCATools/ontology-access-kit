# Slot: OBO_foundry_unique_label

URI: [IAO:0000589](http://purl.obolibrary.org/obo/IAO_0000589)




## Inheritance

* [alternative_term](alternative_term.md)
    * **OBO_foundry_unique_label**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms |  no  |
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

* Multivalued: True





## TODOs

* add uniquekey

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: OBO_foundry_unique_label
todos:
- add uniquekey
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: alternative_term
slot_uri: IAO:0000589
multivalued: true
alias: OBO_foundry_unique_label
domain_of:
- HasSynonyms
range: string

```
</details>