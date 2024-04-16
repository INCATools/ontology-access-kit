

# Slot: IEDB_alternative_term

URI: [OBI:9991118](http://purl.obolibrary.org/obo/OBI_9991118)




## Inheritance

* [alternative_term](alternative_term.md)
    * **IEDB_alternative_term**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Class](Class.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Property](Property.md) |  |  no  |
| [Agent](Agent.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: IEDB_alternative_term
from_schema: https://w3id.org/oak/ontology-metadata
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