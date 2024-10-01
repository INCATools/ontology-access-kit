

# Slot: predicate


_The relationship type for the constraint (e.g. in_taxon, never_in taxon)_





URI: [rdf:predicate](http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TaxonConstraint](TaxonConstraint.md) | An individual taxon constraint |  no  |







## Properties

* Range: [PredicateTerm](PredicateTerm.md)





## TODOs

* define a value set of this

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:predicate |
| native | tc:predicate |




## LinkML Source

<details>
```yaml
name: predicate
description: The relationship type for the constraint (e.g. in_taxon, never_in taxon)
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