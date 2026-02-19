

# Slot: comment



URI: [rdfs:comment](http://www.w3.org/2000/01/rdf-schema#comment)




## Inheritance

* [informative_property](informative_property.md)
    * **comment**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Axiom](Axiom.md) | A logical or non-logical statement |  no  |
| [Image](Image.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Agent](Agent.md) |  |  no  |
| [Ontology](Ontology.md) | An OWL ontology |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HasUserInformation](HasUserInformation.md) |  |  no  |
| [Property](Property.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Comments

* in obo format, a term cannot have more than one comment

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:comment |
| native | omoschema:comment |




## LinkML Source

<details>
```yaml
name: comment
comments:
- in obo format, a term cannot have more than one comment
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: informative_property
slot_uri: rdfs:comment
alias: comment
domain_of:
- HasUserInformation
- Ontology
- Axiom
range: string
multivalued: true

```
</details>