

# Slot: consider



URI: [oio:consider](http://www.geneontology.org/formats/oboInOwl#consider)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **consider**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Class](Class.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HasLifeCycle](HasLifeCycle.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Property](Property.md) |  |  no  |
| [Agent](Agent.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Image](Image.md) |  |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |







## Properties

* Range: [Any](Any.md)

* Multivalued: True





## Comments

* {'RULE': 'subject must be deprecated'}

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oio:consider |
| native | omoschema:consider |




## LinkML Source

<details>
```yaml
name: consider
comments:
- '{''RULE'': ''subject must be deprecated''}'
in_subset:
- go permitted profile
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: obsoletion_related_property
domain: ObsoleteAspect
slot_uri: oio:consider
alias: consider
domain_of:
- HasLifeCycle
range: Any
multivalued: true

```
</details>