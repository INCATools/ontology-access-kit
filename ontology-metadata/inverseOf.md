

# Slot: inverseOf



URI: [owl:inverseOf](http://www.w3.org/2002/07/owl#inverseOf)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **inverseOf**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |







## Properties

* Range: [Property](Property.md)





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:inverseOf |
| native | omoschema:inverseOf |




## LinkML Source

<details>
```yaml
name: inverseOf
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: logical_predicate
slot_uri: owl:inverseOf
alias: inverseOf
domain_of:
- ObjectProperty
range: Property

```
</details>