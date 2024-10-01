

# Slot: annotatedTarget



URI: [owl:annotatedTarget](http://www.w3.org/2002/07/owl#annotatedTarget)




## Inheritance

* [reification_predicate](reification_predicate.md)
    * **annotatedTarget**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Axiom](Axiom.md) | A logical or non-logical statement |  no  |







## Properties

* Range: [Any](Any.md)





## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:annotatedTarget |
| native | omoschema:annotatedTarget |
| exact | rdf:object |




## LinkML Source

<details>
```yaml
name: annotatedTarget
todos:
- restrict range
from_schema: https://w3id.org/oak/ontology-metadata
exact_mappings:
- rdf:object
rank: 1000
is_a: reification_predicate
slot_uri: owl:annotatedTarget
alias: annotatedTarget
domain_of:
- Axiom
relational_role: OBJECT
range: Any

```
</details>