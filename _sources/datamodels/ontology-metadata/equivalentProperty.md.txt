# Slot: equivalentProperty

URI: [http://www.w3.org/2002/07/owl#equivalentProperty](http://www.w3.org/2002/07/owl#equivalentProperty)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **equivalentProperty** [ [match_aspect](match_aspect.md)]





## Properties

* Range: [Property](Property.md)
* Multivalued: True







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Specification

<details>
```yaml
name: equivalentProperty
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
mixins:
- match_aspect
slot_uri: owl:equivalentProperty
multivalued: true
alias: equivalentProperty
domain_of:
- ObjectProperty
range: Property

```
</details>