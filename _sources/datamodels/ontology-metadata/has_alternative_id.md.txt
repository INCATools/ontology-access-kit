# Slot: has_alternative_id


_Relates a live term to a deprecated ID that was merged in_



URI: [oio:hasAlternativeId](http://www.geneontology.org/formats/oboInOwl#hasAlternativeId)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **has_alternative_id**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[HasLifeCycle](HasLifeCycle.md) |  |  no  |
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
[Class](Class.md) |  |  no  |
[Property](Property.md) |  |  no  |
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
[HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
[Agent](Agent.md) |  |  no  |
[Image](Image.md) |  |  no  |
[Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Multivalued: True





## Comments

* {'RULE': 'object must NOT be deprecated'}

## See Also

* [https://github.com/owlcs/owlapi/issues/317](https://github.com/owlcs/owlapi/issues/317)

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




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
from_schema: http://purl.obolibrary.org/obo/omo/schema
see_also:
- https://github.com/owlcs/owlapi/issues/317
rank: 1000
is_a: obsoletion_related_property
domain: NotObsoleteAspect
slot_uri: oio:hasAlternativeId
multivalued: true
alias: has_alternative_id
domain_of:
- HasLifeCycle
range: uriorcurie

```
</details>