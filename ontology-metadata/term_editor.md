

# Slot: term_editor

URI: [IAO:0000117](http://purl.obolibrary.org/obo/IAO_0000117)




## Inheritance

* [provenance_property](provenance_property.md)
    * **term_editor**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Property](Property.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Image](Image.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Agent](Agent.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: term_editor
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: provenance_property
slot_uri: IAO:0000117
multivalued: true
alias: term_editor
domain_of:
- HasProvenance
range: string

```
</details>