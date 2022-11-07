# Slot: OBO_foundry_unique_label

URI: [IAO:0000589](http://purl.obolibrary.org/obo/IAO_0000589)




## Inheritance

* [alternative_term](alternative_term.md)
    * **OBO_foundry_unique_label**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | None
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[Subset](Subset.md) | A collection of terms grouped for some purpose






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## Alias




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