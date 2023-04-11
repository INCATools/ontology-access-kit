# Slot: term_replaced_by

URI: [IAO:0100001](http://purl.obolibrary.org/obo/IAO_0100001)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **term_replaced_by**





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

* Range: [Any](Any.md)







## Comments

* {'RULE': 'subject must be deprecated'}

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




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
from_schema: http://purl.obolibrary.org/obo/omo/schema
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