# Slot: annotatedSource

URI: [http://www.w3.org/2002/07/owl#annotatedSource](http://www.w3.org/2002/07/owl#annotatedSource)




## Inheritance

* [reification_predicate](reification_predicate.md)
    * **annotatedSource**





## Properties

* Range: [NamedObject](NamedObject.md)
* Multivalued: None







## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: annotatedSource
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- rdf:subject
rank: 1000
is_a: reification_predicate
slot_uri: owl:annotatedSource
alias: annotatedSource
domain_of:
- Axiom
relational_role: SUBJECT
range: NamedObject

```
</details>