# Slot: by_ontology
_statistics keyed by ontology_


URI: [reporting:by_ontology](https://w3id.org/linkml/reportby_ontology)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[GlobalStatistics](GlobalStatistics.md) | summary statistics for the entire resource






## Properties

* Range: [FacetStatistics](FacetStatistics.md)
* Multivalued: True







## Alias




## Comments

* if a large ontology collection like OntoBee is indexed then it makes sense to break stats into each sub-ontology

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: by_ontology
description: statistics keyed by ontology
comments:
- if a large ontology collection like OntoBee is indexed then it makes sense to break
  stats into each sub-ontology
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
multivalued: true
alias: by_ontology
owner: GlobalStatistics
domain_of:
- GlobalStatistics
range: FacetStatistics
inlined: true

```
</details>