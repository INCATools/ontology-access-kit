# Slot: creation_date

URI: [oio:creation_date](http://www.geneontology.org/formats/oboInOwl#creation_date)




## Inheritance

* [provenance_property](provenance_property.md)
    * **creation_date**





## Applicable Classes

| Name | Description |
| --- | --- |
[HasProvenance](HasProvenance.md) | None
[Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies
[Class](Class.md) | None
[Property](Property.md) | None
[AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity
[NamedIndividual](NamedIndividual.md) | An instance that has a IRI
[Subset](Subset.md) | A collection of terms grouped for some purpose






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## Alias




## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: creation_date
deprecated: proposed obsoleted by OMO group 2022-04-12
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
deprecated_element_has_exact_replacement: created
rank: 1000
is_a: provenance_property
slot_uri: oio:creation_date
multivalued: true
alias: creation_date
domain_of:
- HasProvenance
range: string

```
</details>