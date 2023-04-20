# Slot: IEDB_alternative_term

URI: [OBI:9991118](http://purl.obolibrary.org/obo/OBI_9991118)




## Inheritance

* [alternative_term](alternative_term.md)
    * **IEDB_alternative_term**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms
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
name: IEDB_alternative_term
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: alternative_term
slot_uri: OBI:9991118
multivalued: true
alias: IEDB_alternative_term
domain_of:
- HasSynonyms
range: string

```
</details>