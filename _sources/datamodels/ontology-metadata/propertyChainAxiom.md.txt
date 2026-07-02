

# Slot: propertyChainAxiom



URI: [owl:propertyChainAxiom](http://www.w3.org/2002/07/owl#propertyChainAxiom)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **propertyChainAxiom**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity |  no  |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:propertyChainAxiom |
| native | omoschema:propertyChainAxiom |




## LinkML Source

<details>
```yaml
name: propertyChainAxiom
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: logical_predicate
slot_uri: owl:propertyChainAxiom
alias: propertyChainAxiom
domain_of:
- ObjectProperty
range: string
multivalued: true

```
</details>