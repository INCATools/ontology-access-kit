

# Slot: excluded_subClassOf

URI: [omoschema:excluded_subClassOf](https://w3id.org/oak/ontology-metadata/excluded_subClassOf)




## Inheritance

* [excluded_axiom](excluded_axiom.md)
    * **excluded_subClassOf**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Image](Image.md) |  |  no  |
| [Property](Property.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Agent](Agent.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [HasLifeCycle](HasLifeCycle.md) |  |  no  |







## Properties

* Range: [Class](Class.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## LinkML Source

<details>
```yaml
name: excluded_subClassOf
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: excluded_axiom
multivalued: true
alias: excluded_subClassOf
domain_of:
- HasLifeCycle
range: Class

```
</details>