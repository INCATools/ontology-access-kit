

# Slot: has_exact_synonym

URI: [oio:hasExactSynonym](http://www.geneontology.org/formats/oboInOwl#hasExactSynonym)




## Inheritance

* [alternative_term](alternative_term.md)
    * [synonym](synonym.md)
        * **has_exact_synonym**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Property](Property.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Image](Image.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Agent](Agent.md) |  |  no  |
| [Axiom](Axiom.md) | A logical or non-logical statement |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |







## Properties

* Range: [LabelType](LabelType.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: has_exact_synonym
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: synonym
slot_uri: oio:hasExactSynonym
multivalued: true
alias: has_exact_synonym
domain_of:
- HasSynonyms
- Axiom
disjoint_with:
- label
range: label type

```
</details>