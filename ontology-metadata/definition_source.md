

# Slot: definition_source



URI: [IAO:0000119](http://purl.obolibrary.org/obo/IAO_0000119)




## Inheritance

* [provenance_property](provenance_property.md)
    * **definition_source**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |
| [Agent](Agent.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Property](Property.md) |  |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Image](Image.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | IAO:0000119 |
| native | omoschema:definition_source |




## LinkML Source

<details>
```yaml
name: definition_source
todos:
- restrict range
in_subset:
- obi permitted profile
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: provenance_property
slot_uri: IAO:0000119
alias: definition_source
domain_of:
- HasProvenance
range: string
multivalued: true

```
</details>