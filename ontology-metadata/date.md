

# Slot: date


_when the term was updated_



URI: [dcterms:date](http://purl.org/dc/terms/date)




## Inheritance

* [provenance_property](provenance_property.md)
    * **date**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Class](Class.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Property](Property.md) |  |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |
| [Agent](Agent.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: date
description: when the term was updated
from_schema: https://w3id.org/oak/ontology-metadata
close_mappings:
- pav:authoredOn
rank: 1000
is_a: provenance_property
slot_uri: dcterms:date
multivalued: true
alias: date
domain_of:
- HasProvenance
range: string

```
</details>