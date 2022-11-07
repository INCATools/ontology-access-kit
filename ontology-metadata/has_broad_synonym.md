# Slot: has_broad_synonym

URI: [oio:hasBroadSynonym](http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym)




## Inheritance

* [alternative_term](alternative_term.md)
    * [synonym](synonym.md)
        * **has_broad_synonym**





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

* Range: [LabelType](LabelType.md)
* Multivalued: True







## Alias




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