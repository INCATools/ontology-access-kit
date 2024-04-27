

# Slot: contributor

URI: [dcterms:contributor](http://purl.org/dc/terms/contributor)




## Inheritance

* [provenance_property](provenance_property.md)
    * **contributor**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Property](Property.md) |  |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Agent](Agent.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |







## Properties

* Range: [Agent](Agent.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: contributor
from_schema: https://w3id.org/oak/ontology-metadata
close_mappings:
- prov:wasAttributedTo
rank: 1000
is_a: provenance_property
slot_uri: dcterms:contributor
multivalued: true
alias: contributor
domain_of:
- HasProvenance
range: Agent
structured_pattern:
  syntax: '{orcid_regex}'
  interpolated: true
  partial_match: false

```
</details>