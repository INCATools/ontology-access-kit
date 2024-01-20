# Slot: source

URI: [dcterms:source](http://purl.org/dc/terms/source)




## Inheritance

* [provenance_property](provenance_property.md)
    * **source**





## Applicable Classes

| Name | Description |
| --- | --- |
[Ontology](Ontology.md) | An OWL ontology
[Axiom](Axiom.md) | A logical or non-logical statement






## Properties

* Range: [String](String.md)
* Multivalued: True








## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: source
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- http://purl.org/dc/terms/source
- oio:source
rank: 1000
is_a: provenance_property
slot_uri: dcterms:source
multivalued: true
alias: source
domain_of:
- Ontology
- Axiom
range: string

```
</details>