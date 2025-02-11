

# Slot: date


_when the term was updated_





URI: [dcterms:date](http://purl.org/dc/terms/date)




## Inheritance

* [provenance_property](provenance_property.md)
    * **date**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Class](Class.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Agent](Agent.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Image](Image.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |
| [Property](Property.md) |  |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcterms:date |
| native | omoschema:date |
| close | pav:authoredOn |




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
alias: date
domain_of:
- HasProvenance
range: string
multivalued: true

```
</details>