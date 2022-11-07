# Slot: alternative_term

URI: [IAO:0000118](http://purl.obolibrary.org/obo/IAO_0000118)




## Inheritance

* **alternative_term**
    * [ISA_alternative_term](ISA_alternative_term.md)
    * [IEDB_alternative_term](IEDB_alternative_term.md)
    * [OBO_foundry_unique_label](OBO_foundry_unique_label.md)
    * [synonym](synonym.md)
    * [editor_preferred_term](editor_preferred_term.md)





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




## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: alternative_term
in_subset:
- allotrope permitted profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- skos:altLabel
rank: 1000
slot_uri: IAO:0000118
multivalued: true
alias: alternative_term
domain_of:
- HasSynonyms
range: string

```
</details>