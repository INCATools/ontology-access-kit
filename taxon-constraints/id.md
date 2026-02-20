

# Slot: id


_the OBO CURIE for the term_





URI: [tc:id](https://w3id.org/linkml/taxon_constraints/id)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Term](Term.md) | An ontology term |  no  |
| [SubjectTerm](SubjectTerm.md) | A term that is the subject of a taxon constraint |  no  |
| [PredicateTerm](PredicateTerm.md) | A term that represents a relationship type |  no  |
| [Taxon](Taxon.md) | A term that represents a taxonomic group, may be at species level of a higher... |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | tc:id |
| native | tc:id |




## LinkML Source

<details>
```yaml
name: id
description: the OBO CURIE for the term
from_schema: https://w3id.org/oak/taxon_constraints
rank: 1000
identifier: true
alias: id
owner: Term
domain_of:
- Term
range: uriorcurie
required: true

```
</details>