

# Slot: example_of_usage



URI: [IAO:0000112](http://purl.obolibrary.org/obo/IAO_0000112)




## Inheritance

* [informative_property](informative_property.md)
    * **example_of_usage**






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
| [Class](Class.md) |  |  no  |
| [HasUserInformation](HasUserInformation.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | IAO:0000112 |
| native | omoschema:example_of_usage |
| exact | skos:example |




## LinkML Source

<details>
```yaml
name: example_of_usage
in_subset:
- allotrope permitted profile
from_schema: https://w3id.org/oak/ontology-metadata
exact_mappings:
- skos:example
rank: 1000
is_a: informative_property
slot_uri: IAO:0000112
alias: example_of_usage
domain_of:
- HasUserInformation
range: string
multivalued: true

```
</details>