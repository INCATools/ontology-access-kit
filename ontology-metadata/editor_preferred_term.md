

# Slot: editor_preferred_term

URI: [IAO:0000111](http://purl.obolibrary.org/obo/IAO_0000111)




## Inheritance

* [alternative_term](alternative_term.md)
    * **editor_preferred_term**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Image](Image.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Property](Property.md) |  |  no  |
| [Agent](Agent.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: editor_preferred_term
in_subset:
- obi permitted profile
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: alternative_term
slot_uri: IAO:0000111
multivalued: true
alias: editor_preferred_term
domain_of:
- HasSynonyms
range: string

```
</details>