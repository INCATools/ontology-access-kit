# Slot: predicate
_The relationship type for the contraint (e.g. in_taxon, never_in taxon)_


URI: [rdf:predicate](http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[TaxonConstraint](TaxonConstraint.md) | An individual taxon constraint






## Properties

* Range: [PredicateTerm](PredicateTerm.md)







## TODOs

* define a value set of this

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## LinkML Source

<details>
```yaml
name: predicate
description: The relationship type for the contraint (e.g. in_taxon, never_in taxon)
todos:
- define a value set of this
from_schema: https://w3id.org/oak/taxon_constraints
rank: 1000
slot_uri: rdf:predicate
alias: predicate
owner: TaxonConstraint
domain_of:
- TaxonConstraint
range: PredicateTerm

```
</details>