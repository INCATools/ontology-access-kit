

# Slot: curator_note



URI: [IAO:0000232](http://purl.obolibrary.org/obo/IAO_0000232)




## Inheritance

* [provenance_property](provenance_property.md)
    * **curator_note**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Class](Class.md) |  |  no  |
| [Property](Property.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [HasUserInformation](HasUserInformation.md) |  |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Image](Image.md) |  |  no  |
| [Agent](Agent.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | IAO:0000232 |
| native | omoschema:curator_note |




## LinkML Source

<details>
```yaml
name: curator_note
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: provenance_property
slot_uri: IAO:0000232
alias: curator_note
domain_of:
- HasUserInformation
range: string
multivalued: true

```
</details>