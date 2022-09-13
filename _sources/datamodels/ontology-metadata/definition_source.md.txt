# Slot: definition_source

URI: [http://purl.obolibrary.org/obo/IAO_0000119](http://purl.obolibrary.org/obo/IAO_0000119)




## Inheritance

* [provenance_property](provenance_property.md)
    * **definition_source**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True







## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: definition_source
todos:
- restrict range
in_subset:
- obi permitted profile
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: provenance_property
slot_uri: IAO:0000119
multivalued: true
alias: definition_source
domain_of:
- HasProvenance
range: string

```
</details>