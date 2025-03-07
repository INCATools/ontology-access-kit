

# Slot: in_subset


_Maps an ontology element to a subset it belongs to_





URI: [oio:inSubset](http://www.geneontology.org/formats/oboInOwl#inSubset)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Class](Class.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Agent](Agent.md) |  |  no  |
| [HasCategory](HasCategory.md) |  |  no  |
| [Property](Property.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Image](Image.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |







## Properties

* Range: [Subset](Subset.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oio:inSubset |
| native | omoschema:in_subset |




## LinkML Source

<details>
```yaml
name: in_subset
description: Maps an ontology element to a subset it belongs to
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
slot_uri: oio:inSubset
alias: in_subset
domain_of:
- HasCategory
range: Subset
multivalued: true

```
</details>