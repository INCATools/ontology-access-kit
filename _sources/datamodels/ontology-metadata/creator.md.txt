# Slot: creator

URI: [http://purl.org/dc/terms/creator](http://purl.org/dc/terms/creator)




## Inheritance

* [provenance_property](provenance_property.md)
    * **creator**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: creator
from_schema: http://purl.obolibrary.org/obo/omo/schema
close_mappings:
- prov:wasAttributedTo
rank: 1000
is_a: provenance_property
slot_uri: dcterms:creator
multivalued: true
alias: creator
domain_of:
- HasProvenance
- Ontology
range: string

```
</details>