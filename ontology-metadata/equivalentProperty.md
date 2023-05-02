# Slot: equivalentProperty

URI: [owl:equivalentProperty](http://www.w3.org/2002/07/owl#equivalentProperty)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **equivalentProperty** [ [match_aspect](match_aspect.md)]





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |







## Properties

* Range: [Property](Property.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

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