

# Slot: database_cross_reference

URI: [oio:hasDbXref](http://www.geneontology.org/formats/oboInOwl#hasDbXref)




## Inheritance

* [match](match.md) [ [match_aspect](match_aspect.md)]
    * **database_cross_reference**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Property](Property.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Class](Class.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [Agent](Agent.md) |  |  no  |
| [HasMappings](HasMappings.md) |  |  no  |
| [Axiom](Axiom.md) | A logical or non-logical statement |  yes  |







## Properties

* Range: [CURIELiteral](CURIELiteral.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: database_cross_reference
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: match
slot_uri: oio:hasDbXref
multivalued: true
alias: database_cross_reference
domain_of:
- HasMappings
- Axiom
range: CURIELiteral

```
</details>