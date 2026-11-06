

# Slot: source



URI: [dcterms:source](http://purl.org/dc/terms/source)




## Inheritance

* [provenance_property](provenance_property.md)
    * **source**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Axiom](Axiom.md) | A logical or non-logical statement |  no  |
| [Ontology](Ontology.md) | An OWL ontology |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dcterms:source |
| native | omoschema:source |
| exact | http://purl.org/dc/terms/source, oio:source |




## LinkML Source

<details>
```yaml
name: source
from_schema: https://w3id.org/oak/ontology-metadata
exact_mappings:
- http://purl.org/dc/terms/source
- oio:source
rank: 1000
is_a: provenance_property
slot_uri: dcterms:source
alias: source
domain_of:
- Ontology
- Axiom
range: string
multivalued: true

```
</details>