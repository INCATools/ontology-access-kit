# Slot: has_alternative_id
_Relates a live term to a deprecated ID that was merged in_


URI: [oio:hasAlternativeId](http://www.geneontology.org/formats/oboInOwl#hasAlternativeId)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **has_alternative_id**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasLifeCycle](HasLifeCycle.md) | 
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | 
[Property](Property.md) | 
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[HomoSapiens](HomoSapiens.md) | An individual human being
[Agent](Agent.md) | 
[Image](Image.md) | 
[Subset](Subset.md) | A collection of terms grouped for some purpose






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