# Slot: excluded_subClassOf

URI: [omoschema:excluded_subClassOf](http://purl.obolibrary.org/obo/omo/schema/excluded_subClassOf)




## Inheritance

* [excluded_axiom](excluded_axiom.md)
    * **excluded_subClassOf**





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

* Range: [Class](Class.md)
* Multivalued: True








## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: excluded_subClassOf
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: excluded_axiom
multivalued: true
alias: excluded_subClassOf
domain_of:
- HasLifeCycle
range: Class

```
</details>