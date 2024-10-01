

# Slot: annotatedSource



URI: [owl:annotatedSource](http://www.w3.org/2002/07/owl#annotatedSource)




## Inheritance

* [reification_predicate](reification_predicate.md)
    * **annotatedSource**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Axiom](Axiom.md) | A logical or non-logical statement |  no  |







## Properties

* Range: [NamedObject](NamedObject.md)





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:annotatedSource |
| native | omoschema:annotatedSource |
| exact | rdf:subject |




## LinkML Source

<details>
```yaml
name: annotatedSource
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
exact_mappings:
- rdf:subject
rank: 1000
is_a: reification_predicate
slot_uri: owl:annotatedSource
alias: annotatedSource
domain_of:
- Axiom
relational_role: SUBJECT
range: NamedObject

```
</details>