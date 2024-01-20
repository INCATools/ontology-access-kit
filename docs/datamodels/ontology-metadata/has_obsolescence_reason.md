# Slot: has_obsolescence_reason

URI: [IAO:0000231](http://purl.obolibrary.org/obo/IAO_0000231)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **has_obsolescence_reason**





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

* Range: [String](String.md)







## Comments

* {'RULE': 'subject must be deprecated'}

## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: has_obsolescence_reason
todos:
- restrict range
comments:
- '{''RULE'': ''subject must be deprecated''}'
from_schema: http://purl.obolibrary.org/obo/omo/schema
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