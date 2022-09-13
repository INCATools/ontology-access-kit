# Slot: contributor

URI: [http://purl.org/dc/terms/contributor](http://purl.org/dc/terms/contributor)




## Inheritance

* [provenance_property](provenance_property.md)
    * **contributor**





## Properties

* Range: [Thing](Thing.md)
* Multivalued: True







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: contributor
from_schema: http://purl.obolibrary.org/obo/omo/schema
close_mappings:
- prov:wasAttributedTo
rank: 1000
is_a: provenance_property
slot_uri: dcterms:contributor
multivalued: true
alias: contributor
domain_of:
- HasProvenance
range: Thing

```
</details>