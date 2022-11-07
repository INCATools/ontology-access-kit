# Slot: in_subset
_Maps an ontology element to a subset it belongs to_


URI: [oio:inSubset](http://www.geneontology.org/formats/oboInOwl#inSubset)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[HasCategory](HasCategory.md) | None
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | None
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[Subset](Subset.md) | A collection of terms grouped for some purpose






## Properties

* Range: [Subset](Subset.md)
* Multivalued: True







## Alias




## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: in_subset
description: Maps an ontology element to a subset it belongs to
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
slot_uri: oio:inSubset
multivalued: true
alias: in_subset
domain_of:
- HasCategory
range: Subset

```
</details>