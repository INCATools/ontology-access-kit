

# Slot: has_obo_namespace



URI: [oio:hasOBONamespace](http://www.geneontology.org/formats/oboInOwl#hasOBONamespace)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Property](Property.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Agent](Agent.md) |  |  no  |
| [HasCategory](HasCategory.md) |  |  no  |
| [Image](Image.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Class](Class.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
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
| self | oio:hasOBONamespace |
| native | omoschema:has_obo_namespace |




## LinkML Source

<details>
```yaml
name: has_obo_namespace
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
slot_uri: oio:hasOBONamespace
alias: has_obo_namespace
domain_of:
- HasCategory
range: string
multivalued: true

```
</details>