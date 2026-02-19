

# Slot: id


_this maps to the URI in RDF_





URI: [omoschema:id](https://w3id.org/oak/ontology-metadata/id)




## Inheritance

* [core_property](core_property.md)
    * **id**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Class](Class.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  yes  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Agent](Agent.md) |  |  yes  |
| [Ontology](Ontology.md) | An OWL ontology |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Image](Image.md) |  |  no  |
| [NamedObject](NamedObject.md) | Anything with an IRI |  no  |
| [Property](Property.md) |  |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:id |
| native | omoschema:id |




## LinkML Source

<details>
```yaml
name: id
description: this maps to the URI in RDF
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: core_property
identifier: true
alias: id
domain_of:
- NamedObject
range: uriorcurie
required: true

```
</details>