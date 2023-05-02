# Slot: created


_when the term came into being_



URI: [dcterms:created](http://purl.org/dc/terms/created)




## Inheritance

* [provenance_property](provenance_property.md)
    * **created**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[HasProvenance](HasProvenance.md) |  |  no  |
[Ontology](Ontology.md) | An OWL ontology |  no  |
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

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: created
description: when the term came into being
from_schema: http://purl.obolibrary.org/obo/omo/schema
close_mappings:
- pav:createdOn
rank: 1000
is_a: provenance_property
slot_uri: dcterms:created
multivalued: false
alias: created
domain_of:
- HasProvenance
- Ontology
range: string

```
</details>