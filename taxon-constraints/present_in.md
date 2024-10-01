

# Slot: present_in


_The term MAY be in the specified taxon, or a descendant of that taxon_

__





URI: [RO:0002175](http://purl.obolibrary.org/obo/RO_0002175)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SubjectTerm](SubjectTerm.md) | A term that is the subject of a taxon constraint |  no  |







## Properties

* Range: [TaxonConstraint](TaxonConstraint.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | RO:0002175 |
| native | tc:present_in |




## LinkML Source

<details>
```yaml
name: present_in
description: 'The term MAY be in the specified taxon, or a descendant of that taxon

  '
from_schema: https://w3id.org/oak/taxon_constraints
rank: 1000
slot_uri: RO:0002175
alias: present_in
owner: SubjectTerm
domain_of:
- SubjectTerm
range: TaxonConstraint
multivalued: true

```
</details>