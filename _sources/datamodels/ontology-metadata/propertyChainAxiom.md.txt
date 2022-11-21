# Slot: propertyChainAxiom

URI: [owl:propertyChainAxiom](http://www.w3.org/2002/07/owl#propertyChainAxiom)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **propertyChainAxiom**





## Applicable Classes

| Name | Description |
| --- | --- |
[ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms
[TransitiveProperty](TransitiveProperty.md) | An ObjectProperty with the property of transitivity






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: True








## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: propertyChainAxiom
todos:
- restrict range
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
slot_uri: owl:propertyChainAxiom
multivalued: true
alias: propertyChainAxiom
domain_of:
- ObjectProperty
range: string

```
</details>