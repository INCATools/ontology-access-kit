

# Slot: annotatedProperty



URI: [owl:annotatedProperty](http://www.w3.org/2002/07/owl#annotatedProperty)




## Inheritance

* [reification_predicate](reification_predicate.md)
    * **annotatedProperty**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Axiom](Axiom.md) | A logical or non-logical statement |  no  |







## Properties

* Range: [AnnotationProperty](AnnotationProperty.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:annotatedProperty |
| native | omoschema:annotatedProperty |
| exact | rdf:predicate |




## LinkML Source

<details>
```yaml
name: annotatedProperty
from_schema: https://w3id.org/oak/ontology-metadata
exact_mappings:
- rdf:predicate
rank: 1000
is_a: reification_predicate
slot_uri: owl:annotatedProperty
alias: annotatedProperty
domain_of:
- Axiom
relational_role: PREDICATE
range: AnnotationProperty

```
</details>