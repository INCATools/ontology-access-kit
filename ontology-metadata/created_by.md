

# Slot: created_by



URI: [oio:created_by](http://www.geneontology.org/formats/oboInOwl#created_by)




## Inheritance

* [provenance_property](provenance_property.md)
    * **created_by**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [HomoSapiens](HomoSapiens.md) | An individual human being |  no  |
| [Agent](Agent.md) |  |  no  |
| [Property](Property.md) |  |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
| [HasProvenance](HasProvenance.md) |  |  no  |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |  no  |
| [NamedIndividual](NamedIndividual.md) | An instance that has a IRI |  no  |
| [Class](Class.md) |  |  no  |
| [AnnotationProperty](AnnotationProperty.md) | A property used in non-logical axioms |  no  |
| [Axiom](Axiom.md) | A logical or non-logical statement |  no  |
| [Image](Image.md) |  |  no  |
| [Subset](Subset.md) | A collection of terms grouped for some purpose |  no  |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oio:created_by |
| native | omoschema:created_by |




## LinkML Source

<details>
```yaml
name: created_by
deprecated: proposed obsoleted by OMO group 2022-04-12
from_schema: https://w3id.org/oak/ontology-metadata
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