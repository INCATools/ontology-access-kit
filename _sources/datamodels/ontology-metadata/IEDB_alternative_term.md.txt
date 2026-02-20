

# Slot: IEDB_alternative_term



URI: [OBI:9991118](http://purl.obolibrary.org/obo/OBI_9991118)




## Inheritance

* [alternative_term](alternative_term.md)
    * **IEDB_alternative_term**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Agent](Agent.md) |  |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Property](Property.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | OBI:9991118 |
| native | omoschema:IEDB_alternative_term |




## LinkML Source

<details>
```yaml
name: IEDB_alternative_term
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: alternative_term
slot_uri: OBI:9991118
alias: IEDB_alternative_term
domain_of:
- HasSynonyms
range: string
multivalued: true

```
</details>