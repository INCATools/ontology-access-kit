

# Slot: imported_from

URI: [IAO:0000412](http://purl.obolibrary.org/obo/IAO_0000412)




## Inheritance

* [provenance_property](provenance_property.md)
    * **imported_from**






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

* Range: [NamedIndividual](NamedIndividual.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: imported_from
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: provenance_property
slot_uri: IAO:0000412
multivalued: true
alias: imported_from
domain_of:
- HasProvenance
range: NamedIndividual

```
</details>