

# Slot: excluded_subClassOf



URI: [omoschema:excluded_subClassOf](https://w3id.org/oak/ontology-metadata/excluded_subClassOf)




## Inheritance

* [excluded_axiom](excluded_axiom.md)
    * **excluded_subClassOf**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Class](Class.md) |  |  no  |
| [Agent](Agent.md) |  |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Image](Image.md) |  |  no  |
| [HasLifeCycle](HasLifeCycle.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Property](Property.md) |  |  no  |







## Properties

* Range: [Class](Class.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:excluded_subClassOf |
| native | omoschema:excluded_subClassOf |




## LinkML Source

<details>
```yaml
name: excluded_subClassOf
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: excluded_axiom
alias: excluded_subClassOf
domain_of:
- HasLifeCycle
range: Class
multivalued: true

```
</details>