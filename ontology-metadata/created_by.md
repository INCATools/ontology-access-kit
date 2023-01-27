# Slot: created_by

URI: [oio:created_by](http://www.geneontology.org/formats/oboInOwl#created_by)




## Inheritance

* [provenance_property](provenance_property.md)
    * **created_by**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasProvenance](HasProvenance.md) | 
[Axiom](Axiom.md) | A logical or non-logical statement
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

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: created_by
deprecated: proposed obsoleted by OMO group 2022-04-12
from_schema: http://purl.obolibrary.org/obo/omo/schema
deprecated_element_has_exact_replacement: creator
rank: 1000
is_a: provenance_property
slot_uri: oio:created_by
alias: created_by
domain_of:
- HasProvenance
- Axiom
range: string

```
</details>