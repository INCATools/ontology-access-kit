# Slot: date
_when the term was updated_


URI: [http://purl.org/dc/terms/date](http://purl.org/dc/terms/date)




## Inheritance

* [provenance_property](provenance_property.md)
    * **date**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: date
description: when the term was updated
from_schema: http://purl.obolibrary.org/obo/omo/schema
close_mappings:
- pav:authoredOn
rank: 1000
is_a: provenance_property
slot_uri: dcterms:date
multivalued: true
alias: date
domain_of:
- HasProvenance
range: string

```
</details>