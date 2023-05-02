# Slot: has_broad_synonym

URI: [oio:hasBroadSynonym](http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym)




## Inheritance

* [alternative_term](alternative_term.md)
    * [synonym](synonym.md)
        * **has_broad_synonym**





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

* Range: [LabelType](LabelType.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: has_broad_synonym
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: synonym
slot_uri: oio:hasBroadSynonym
multivalued: true
alias: has_broad_synonym
domain_of:
- HasSynonyms
range: label type

```
</details>