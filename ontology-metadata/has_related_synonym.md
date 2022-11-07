# Slot: has_related_synonym

URI: [oio:hasRelatedSynonym](http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym)



<!-- no inheritance hierarchy -->




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
name: has_related_synonym
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
slot_uri: oio:hasRelatedSynonym
multivalued: true
alias: has_related_synonym
domain_of:
- HasSynonyms
range: label type

```
</details>