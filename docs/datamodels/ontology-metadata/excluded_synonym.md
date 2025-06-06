

# Slot: excluded_synonym



URI: [omoschema:excluded_synonym](https://w3id.org/oak/ontology-metadata/excluded_synonym)




## Inheritance

* [excluded_axiom](excluded_axiom.md)
    * **excluded_synonym**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Class](Class.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Agent](Agent.md) |  |  no  |
| [Property](Property.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [HasLifeCycle](HasLifeCycle.md) |  |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Image](Image.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:excluded_synonym |
| native | omoschema:excluded_synonym |
| exact | skos:hiddenSynonym |




## LinkML Source

<details>
```yaml
name: excluded_synonym
from_schema: https://w3id.org/oak/ontology-metadata
exact_mappings:
- skos:hiddenSynonym
rank: 1000
is_a: excluded_axiom
alias: excluded_synonym
domain_of:
- HasLifeCycle
range: string
multivalued: true

```
</details>