

# Slot: isDefinedBy



URI: [rdfs:isDefinedBy](http://www.w3.org/2000/01/rdf-schema#isDefinedBy)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Class](Class.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Agent](Agent.md) |  |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [Property](Property.md) |  |  no  |







## Properties

* Range: [Ontology](Ontology.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:isDefinedBy |
| native | omoschema:isDefinedBy |
| close | pav:importedFrom, dcterms:publisher |




## LinkML Source

<details>
```yaml
name: isDefinedBy
from_schema: https://w3id.org/oak/ontology-metadata
close_mappings:
- pav:importedFrom
- dcterms:publisher
rank: 1000
slot_uri: rdfs:isDefinedBy
alias: isDefinedBy
domain_of:
- HasProvenance
range: Ontology

```
</details>