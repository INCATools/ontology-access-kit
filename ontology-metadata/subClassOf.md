

# Slot: subClassOf



URI: [rdfs:subClassOf](http://www.w3.org/2000/01/rdf-schema#subClassOf)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **subClassOf**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Restriction](Restriction.md) |  |  no  |
| [ClassExpression](ClassExpression.md) |  |  no  |
| [Class](Class.md) |  |  yes  |







## Properties

* Range: [ClassExpression](ClassExpression.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:subClassOf |
| native | omoschema:subClassOf |




## LinkML Source

<details>
```yaml
name: subClassOf
from_schema: https://w3id.org/oak/ontology-metadata
rank: 1000
is_a: logical_predicate
slot_uri: rdfs:subClassOf
alias: subClassOf
domain_of:
- ClassExpression
range: ClassExpression
multivalued: true

```
</details>