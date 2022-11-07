# Slot: database_cross_reference

URI: [oio:hasDbXref](http://www.geneontology.org/formats/oboInOwl#hasDbXref)




## Inheritance

* [match](match.md) [ [match_aspect](match_aspect.md)]
    * **database_cross_reference**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasMappings](HasMappings.md) | None
[Axiom](Axiom.md) | A logical or non-logical statement
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | None
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[Subset](Subset.md) | A collection of terms grouped for some purpose






## Properties

* Range: [CURIELiteral](CURIELiteral.md)
* Multivalued: True







## Alias




## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: database_cross_reference
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: match
slot_uri: oio:hasDbXref
multivalued: true
alias: database_cross_reference
domain_of:
- HasMappings
- Axiom
range: CURIELiteral

```
</details>