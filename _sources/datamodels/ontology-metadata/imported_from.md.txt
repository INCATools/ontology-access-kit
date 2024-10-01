

# Slot: imported_from



URI: [IAO:0000412](http://purl.obolibrary.org/obo/IAO_0000412)




## Inheritance

* [provenance_property](provenance_property.md)
    * **imported_from**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Agent](Agent.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Property](Property.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |







## Properties

* Range: [NamedIndividual](NamedIndividual.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | IAO:0000412 |
| native | omoschema:imported_from |




## LinkML Source

<details>
```yaml
name: imported_from
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: provenance_property
slot_uri: IAO:0000412
alias: imported_from
domain_of:
- HasProvenance
range: NamedIndividual
multivalued: true

```
</details>