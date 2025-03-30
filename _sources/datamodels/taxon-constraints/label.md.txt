

# Slot: label


_the human readable name or label of the term_





URI: [rdfs:label](http://www.w3.org/2000/01/rdf-schema#label)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [PredicateTerm](PredicateTerm.md) | A term that represents a relationship type |  no  |
| [Taxon](Taxon.md) | A term that represents a taxonomic group, may be at species level of a higher... |  no  |
| [SubjectTerm](SubjectTerm.md) | A term that is the subject of a taxon constraint |  no  |
| [Term](Term.md) | An ontology term |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:label |
| native | tc:label |




## LinkML Source

<details>
```yaml
name: label
description: the human readable name or label of the term
from_schema: https://w3id.org/oak/taxon_constraints
rank: 1000
slot_uri: rdfs:label
alias: label
owner: Term
domain_of:
- Term
range: string

```
</details>