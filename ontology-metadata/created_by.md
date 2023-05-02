# Slot: created_by

URI: [oio:created_by](http://www.geneontology.org/formats/oboInOwl#created_by)




## Inheritance

* [provenance_property](provenance_property.md)
    * **created_by**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[HasProvenance](HasProvenance.md) |  |  no  |
[Axiom](Axiom.md) | A logical or non-logical statement |  no  |
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

* Range: [String](String.md)





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