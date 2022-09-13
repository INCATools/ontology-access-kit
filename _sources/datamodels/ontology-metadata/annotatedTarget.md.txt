# Slot: annotatedTarget

URI: [http://www.w3.org/2002/07/owl#annotatedTarget](http://www.w3.org/2002/07/owl#annotatedTarget)




## Inheritance

* [reification_predicate](reification_predicate.md)
    * **annotatedTarget**





## Properties

* Range: [Any](Any.md)
* Multivalued: None







## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: annotatedTarget
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
exact_mappings:
- rdf:object
rank: 1000
is_a: reification_predicate
slot_uri: owl:annotatedTarget
alias: annotatedTarget
domain_of:
- Axiom
relational_role: OBJECT
range: Any

```
</details>