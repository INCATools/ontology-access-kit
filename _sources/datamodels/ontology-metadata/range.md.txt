# Slot: range

URI: [http://www.w3.org/2000/01/rdf-schema#range](http://www.w3.org/2000/01/rdf-schema#range)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **range**





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
name: range
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
slot_uri: rdfs:range
multivalued: true
alias: range
domain_of:
- Property
range: string

```
</details>