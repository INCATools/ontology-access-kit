

# Slot: label



URI: [rdfs:label](http://www.w3.org/2000/01/rdf-schema#label)




## Inheritance

* [core_property](core_property.md)
    * **label**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Axiom](Axiom.md) | A logical or non-logical statement |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Class](Class.md) |  |  yes  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HasMinimalMetadata](HasMinimalMetadata.md) | Absolute minimum metadata model |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Agent](Agent.md) |  |  no  |
| [Property](Property.md) |  |  yes  |
| [Image](Image.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |







## Properties

* Range: [LabelType](LabelType.md)





## Comments

* SHOULD follow OBO label guidelines
* MUST be unique within an ontology
* SHOULD be unique across OBO

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:label |
| native | omoschema:label |
| exact | skos:prefLabel |




## LinkML Source

<details>
```yaml
name: label
comments:
- SHOULD follow OBO label guidelines
- MUST be unique within an ontology
- SHOULD be unique across OBO
in_subset:
- allotrope required profile
- go required profile
- obi required profile
from_schema: https://w3id.org/oak/ontology-metadata
exact_mappings:
- skos:prefLabel
rank: 1000
is_a: core_property
slot_uri: rdfs:label
alias: label
domain_of:
- HasMinimalMetadata
- Axiom
range: label type
multivalued: false

```
</details>