

# Slot: only_in


_Points to a taxon constraint that states the SubjectTerm is ONLY found in a taxon or descendant. Formally, the term AND its descendants MUST be in the specified taxon, or a descendant of that taxon_

__





URI: [RO:0002160](http://purl.obolibrary.org/obo/RO_0002160)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SubjectTerm](SubjectTerm.md) | A term that is the subject of a taxon constraint |  no  |







## Properties

* Range: [TaxonConstraint](TaxonConstraint.md)

* Multivalued: True





## Comments

* Note that we conflate between the RO "only in taxon" and "in taxon" relations here

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | RO:0002160 |
| native | tc:only_in |




## LinkML Source

<details>
```yaml
name: only_in
description: 'Points to a taxon constraint that states the SubjectTerm is ONLY found
  in a taxon or descendant. Formally, the term AND its descendants MUST be in the
  specified taxon, or a descendant of that taxon

  '
comments:
- Note that we conflate between the RO "only in taxon" and "in taxon" relations here
from_schema: https://w3id.org/oak/taxon_constraints
rank: 1000
slot_uri: RO:0002160
alias: only_in
owner: SubjectTerm
domain_of:
- SubjectTerm
range: TaxonConstraint
multivalued: true

```
</details>