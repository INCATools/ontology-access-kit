

# Slot: deprecated



URI: [owl:deprecated](http://www.w3.org/2002/07/owl#deprecated)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **deprecated**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Image](Image.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Agent](Agent.md) |  |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [HasLifeCycle](HasLifeCycle.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Property](Property.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |







## Properties

* Range: [Boolean](Boolean.md)



## Aliases


* is obsolete



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:deprecated |
| native | omoschema:deprecated |




## LinkML Source

<details>
```yaml
name: deprecated
in_subset:
- allotrope permitted profile
- go permitted profile
- obi permitted profile
from_schema: https://w3id.org/oak/ontology-metadata
aliases:
- is obsolete
rank: 1000
is_a: obsoletion_related_property
domain: ObsoleteAspect
slot_uri: owl:deprecated
alias: deprecated
domain_of:
- HasLifeCycle
range: boolean

```
</details>