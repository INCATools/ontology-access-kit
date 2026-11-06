

# Slot: equivalentProperty



URI: [owl:equivalentProperty](http://www.w3.org/2002/07/owl#equivalentProperty)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **equivalentProperty** [ [match_aspect](match_aspect.md)]






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |







## Properties

* Range: [Property](Property.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:equivalentProperty |
| native | omoschema:equivalentProperty |




## LinkML Source

<details>
```yaml
name: equivalentProperty
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: logical_predicate
mixins:
- match_aspect
slot_uri: owl:equivalentProperty
alias: equivalentProperty
domain_of:
- ObjectProperty
range: Property
multivalued: true

```
</details>