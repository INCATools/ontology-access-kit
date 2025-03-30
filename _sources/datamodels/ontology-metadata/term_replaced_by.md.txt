

# Slot: term_replaced_by



URI: [IAO:0100001](http://purl.obolibrary.org/obo/IAO_0100001)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **term_replaced_by**






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

* Range: [Any](Any.md)





## Comments

* {'RULE': 'subject must be deprecated'}

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | IAO:0100001 |
| native | omoschema:term_replaced_by |
| exact | dcterms:isReplacedBy |




## LinkML Source

<details>
```yaml
name: term_replaced_by
comments:
- '{''RULE'': ''subject must be deprecated''}'
in_subset:
- go permitted profile
- obi permitted profile
- allotrope permitted profile
from_schema: https://w3id.org/oak/ontology-metadata
exact_mappings:
- dcterms:isReplacedBy
rank: 1000
is_a: obsoletion_related_property
domain: ObsoleteAspect
slot_uri: IAO:0100001
alias: term_replaced_by
domain_of:
- HasLifeCycle
range: Any

```
</details>