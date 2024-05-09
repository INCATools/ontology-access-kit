

# Slot: seeAlso

URI: [rdfs:seeAlso](http://www.w3.org/2000/01/rdf-schema#seeAlso)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Property](Property.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Agent](Agent.md) |  |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Axiom](Axiom.md) | A logical or non-logical statement |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [Class](Class.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [HasUserInformation](HasUserInformation.md) |  |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |







## Properties

* Range: [Thing](Thing.md)

* Multivalued: True





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: seeAlso
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
slot_uri: rdfs:seeAlso
multivalued: true
alias: seeAlso
domain_of:
- HasUserInformation
- Axiom
range: Thing

```
</details>