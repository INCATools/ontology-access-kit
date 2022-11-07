# Slot: consider

URI: [oio:consider](http://www.geneontology.org/formats/oboInOwl#consider)




## Inheritance

* [obsoletion_related_property](obsoletion_related_property.md)
    * **consider**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasLifeCycle](HasLifeCycle.md) | None
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | None
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[Subset](Subset.md) | A collection of terms grouped for some purpose






## Properties

* Range: [Any](Any.md)
* Multivalued: True







## Alias




## Comments

* {'RULE': 'subject must be deprecated'}

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: consider
comments:
- '{''RULE'': ''subject must be deprecated''}'
in_subset:
- go permitted profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: obsoletion_related_property
domain: ObsoleteAspect
slot_uri: oio:consider
multivalued: true
alias: consider
domain_of:
- HasLifeCycle
range: Any

```
</details>