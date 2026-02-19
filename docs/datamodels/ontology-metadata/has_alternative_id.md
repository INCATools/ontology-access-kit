

# Slot: has_alternative_id


_Relates a live term to a deprecated ID that was merged in_





URI: [oio:hasAlternativeId](http://www.geneontology.org/formats/oboInOwl#hasAlternativeId)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **has_alternative_id**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [HasLifeCycle](HasLifeCycle.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Agent](Agent.md) |  |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [Image](Image.md) |  |  no  |
| [Property](Property.md) |  |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Multivalued: True





## Comments

* {'RULE': 'object must NOT be deprecated'}

## See Also

* [https://github.com/owlcs/owlapi/issues/317](https://github.com/owlcs/owlapi/issues/317)

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oio:hasAlternativeId |
| native | omoschema:has_alternative_id |




## LinkML Source

<details>
```yaml
name: has_alternative_id
description: Relates a live term to a deprecated ID that was merged in
deprecated: This is deprecated as it is redundant with the inverse replaced_by triple
comments:
- '{''RULE'': ''object must NOT be deprecated''}'
in_subset:
- go permitted profile
from_schema: https://w3id.org/oak/ontology-metadata
see_also:
- https://github.com/owlcs/owlapi/issues/317
rank: 1000
is_a: obsoletion_related_property
domain: NotObsoleteAspect
slot_uri: oio:hasAlternativeId
alias: has_alternative_id
domain_of:
- HasLifeCycle
range: uriorcurie
multivalued: true

```
</details>