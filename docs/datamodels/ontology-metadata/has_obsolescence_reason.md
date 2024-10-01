

# Slot: has_obsolescence_reason



URI: [IAO:0000231](http://purl.obolibrary.org/obo/IAO_0000231)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **has_obsolescence_reason**






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





## Comments

* {'RULE': 'subject must be deprecated'}

## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | IAO:0000231 |
| native | omoschema:has_obsolescence_reason |




## LinkML Source

<details>
```yaml
name: has_obsolescence_reason
todos:
- restrict range
comments:
- '{''RULE'': ''subject must be deprecated''}'
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: obsoletion_related_property
domain: ObsoleteAspect
slot_uri: IAO:0000231
alias: has_obsolescence_reason
domain_of:
- HasLifeCycle
range: string

```
</details>