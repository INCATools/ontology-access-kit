# Slot: seeAlso

URI: [rdfs:seeAlso](http://www.w3.org/2000/01/rdf-schema#seeAlso)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[HasUserInformation](HasUserInformation.md) | None
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

* Range: [Thing](Thing.md)
* Multivalued: True







## Alias




## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: seeAlso
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
slot_uri: rdfs:seeAlso
multivalued: true
alias: seeAlso
domain_of:
- HasUserInformation
- Axiom
range: Thing

```
</details>