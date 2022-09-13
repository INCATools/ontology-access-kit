# Slot: complementOf

URI: [http://www.w3.org/2002/07/owl#complementOf](http://www.w3.org/2002/07/owl#complementOf)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **complementOf**





## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: None







## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: complementOf
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
slot_uri: owl:complementOf
alias: complementOf
domain_of:
- ClassExpression
range: string

```
</details>