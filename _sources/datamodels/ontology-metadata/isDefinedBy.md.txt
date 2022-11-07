# Slot: isDefinedBy

URI: [rdfs:isDefinedBy](http://www.w3.org/2000/01/rdf-schema#isDefinedBy)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[HasProvenance](HasProvenance.md) | None
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | None
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[Subset](Subset.md) | A collection of terms grouped for some purpose






## Properties

* Range: [Ontology](Ontology.md)






## Alias




## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: isDefinedBy
from_schema: http://purl.obolibrary.org/obo/omo/schema
close_mappings:
- pav:importedFrom
- dcterms:publisher
rank: 1000
slot_uri: rdfs:isDefinedBy
alias: isDefinedBy
domain_of:
- HasProvenance
range: Ontology

```
</details>