# Slot: created
_when the term came into being_


URI: [http://purl.org/dc/terms/created](http://purl.org/dc/terms/created)




## Inheritance

* [provenance_property](provenance_property.md)
    * **created**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: False







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: created
description: when the term came into being
from_schema: http://purl.obolibrary.org/obo/omo/schema
close_mappings:
- pav:createdOn
rank: 1000
is_a: provenance_property
slot_uri: dcterms:created
multivalued: false
alias: created
domain_of:
- HasProvenance
- Ontology
range: string

```
</details>