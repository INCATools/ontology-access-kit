# Slot: only_in
_The term AND its descendants MUST be in the specified taxon, or a descendant of that taxon
_


URI: [RO:0002160](http://purl.obolibrary.org/obo/RO_0002160)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[SubjectTerm](SubjectTerm.md) | A term that is the subject of a taxon constraint






## Properties

* Range: [TaxonConstraint](TaxonConstraint.md)
* Multivalued: True








## Comments

* Note that we conflate between the RO "only in taxon" and "in taxon" relations here

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/taxon_constraints




## LinkML Source

<details>
```yaml
name: only_in
description: 'The term AND its descendants MUST be in the specified taxon, or a descendant
  of that taxon

  '
comments:
- Note that we conflate between the RO "only in taxon" and "in taxon" relations here
from_schema: https://w3id.org/linkml/taxon_constraints
rank: 1000
slot_uri: RO:0002160
multivalued: true
alias: only_in
owner: SubjectTerm
domain_of:
- SubjectTerm
range: TaxonConstraint

```
</details>