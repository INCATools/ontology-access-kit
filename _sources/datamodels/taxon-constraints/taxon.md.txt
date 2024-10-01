

# Slot: taxon


_The taxon which this constraint is about. May be species or a more general class._





URI: [rdf:object](http://www.w3.org/1999/02/22-rdf-syntax-ns#object)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [TaxonConstraint](TaxonConstraint.md) | An individual taxon constraint |  no  |







## Properties

* Range: [Taxon](Taxon.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/taxon_constraints




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:object |
| native | tc:taxon |




## LinkML Source

<details>
```yaml
name: taxon
description: The taxon which this constraint is about. May be species or a more general
  class.
from_schema: https://w3id.org/oak/taxon_constraints
rank: 1000
slot_uri: rdf:object
alias: taxon
owner: TaxonConstraint
domain_of:
- TaxonConstraint
range: Taxon
inlined: true

```
</details>