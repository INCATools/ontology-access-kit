# Slot: disjointWith

URI: [http://www.w3.org/2002/07/owl#disjointWith](http://www.w3.org/2002/07/owl#disjointWith)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **disjointWith**





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
name: disjointWith
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
slot_uri: owl:disjointWith
multivalued: true
alias: disjointWith
domain_of:
- ClassExpression
- PropertyExpression
range: string

```
</details>