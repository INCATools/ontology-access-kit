# Slot: subClassOf

URI: [rdfs:subClassOf](http://www.w3.org/2000/01/rdf-schema#subClassOf)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **subClassOf**





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
[ClassExpression](ClassExpression.md) |  |  no  |
[Class](Class.md) |  |  yes  |
[Restriction](Restriction.md) |  |  no  |







## Properties

* Range: [ClassExpression](ClassExpression.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
name: subClassOf
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: logical_predicate
slot_uri: rdfs:subClassOf
multivalued: true
alias: subClassOf
domain_of:
- ClassExpression
range: ClassExpression

```
</details>