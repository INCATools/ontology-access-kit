

# Slot: editor_note



URI: [IAO:0000116](http://purl.obolibrary.org/obo/IAO_0000116)




## Inheritance

* [provenance_property](provenance_property.md)
    * **editor_note**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Image](Image.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Agent](Agent.md) |  |  no  |
| [Property](Property.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [Class](Class.md) |  |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |







## Properties

* Range: [NarrativeText](NarrativeText.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | IAO:0000116 |
| native | omoschema:editor_note |




## LinkML Source

<details>
```yaml
name: editor_note
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: provenance_property
slot_uri: IAO:0000116
alias: editor_note
domain_of:
- HasProvenance
range: narrative text
multivalued: true

```
</details>