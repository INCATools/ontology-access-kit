

# Slot: sameAs



URI: [owl:sameAs](http://www.w3.org/2002/07/owl#sameAs)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **sameAs** [ [match_aspect](match_aspect.md)]









## Properties

* Range: [Thing](Thing.md)

* Multivalued: True





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:sameAs |
| native | omoschema:sameAs |




## LinkML Source

<details>
```yaml
name: sameAs
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: logical_predicate
mixins:
- match_aspect
slot_uri: owl:sameAs
alias: sameAs
range: Thing
multivalued: true

```
</details>