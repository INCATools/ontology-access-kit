# Slot: subject
_The term to which the constraint applies_


URI: [rdf:subject](http://www.w3.org/1999/02/22-rdf-syntax-ns#subject)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[TaxonConstraint](TaxonConstraint.md) | An individual taxon constraint






## Properties

* Range: [SubjectTerm](SubjectTerm.md)







## Comments

* this is a reciprocal slot and will be the same as the containing SubjectTerm

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## LinkML Source

<details>
```yaml
name: subject
description: The term to which the constraint applies
comments:
- this is a reciprocal slot and will be the same as the containing SubjectTerm
from_schema: https://w3id.org/oak/taxon_constraints
rank: 1000
slot_uri: rdf:subject
alias: subject
owner: TaxonConstraint
domain_of:
- TaxonConstraint
range: SubjectTerm

```
</details>