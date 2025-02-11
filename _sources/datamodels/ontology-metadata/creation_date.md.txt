

# Slot: creation_date



URI: [oio:creation_date](http://www.geneontology.org/formats/oboInOwl#creation_date)




## Inheritance

* [provenance_property](provenance_property.md)
    * **creation_date**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Class](Class.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [Agent](Agent.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Image](Image.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |
| [Property](Property.md) |  |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oio:creation_date |
| native | omoschema:creation_date |




## LinkML Source

<details>
```yaml
name: creation_date
deprecated: proposed obsoleted by OMO group 2022-04-12
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
deprecated_element_has_exact_replacement: created
rank: 1000
is_a: provenance_property
slot_uri: oio:creation_date
alias: creation_date
domain_of:
- HasProvenance
range: string
multivalued: true

```
</details>