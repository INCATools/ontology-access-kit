# Slot: by_category
_statistics keyed by category_


URI: [reporting:by_category](https://w3id.org/linkml/reportby_category)



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

* for example, GO stats may be broken out by MF/BP/CC

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: by_category
description: statistics keyed by category
comments:
- for example, GO stats may be broken out by MF/BP/CC
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
multivalued: true
alias: by_category
owner: GlobalStatistics
domain_of:
- GlobalStatistics
range: FacetStatistics
inlined: true

```
</details>