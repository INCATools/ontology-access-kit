

# Slot: has_narrow_synonym



URI: [oio:hasNarrowSynonym](http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym)




## Inheritance

* [alternative_term](alternative_term.md)
    * [synonym](synonym.md)
        * **has_narrow_synonym**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Class](Class.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Agent](Agent.md) |  |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HasSynonyms](HasSynonyms.md) | a mixin for a class whose members can have synonyms |  no  |
| [Image](Image.md) |  |  no  |
| [Property](Property.md) |  |  no  |







## Properties

* Range: [LabelType](LabelType.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oio:hasNarrowSynonym |
| native | omoschema:has_narrow_synonym |




## LinkML Source

<details>
```yaml
name: has_narrow_synonym
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: synonym
slot_uri: oio:hasNarrowSynonym
alias: has_narrow_synonym
domain_of:
- HasSynonyms
range: label type
multivalued: true

```
</details>