# Slot: partitions
_statistics keyed by category_


URI: [reporting:partitions](https://w3id.org/linkml/reportpartitions)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[GlobalStatistics](GlobalStatistics.md) | summary statistics for the entire resource






## Properties

* Range: [SummaryStatisticCollection](SummaryStatisticCollection.md)
* Multivalued: True








## Comments

* for example, GO stats may be broken out by MF/BP/CC

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: partitions
description: statistics keyed by category
comments:
- for example, GO stats may be broken out by MF/BP/CC
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
multivalued: true
alias: partitions
owner: GlobalStatistics
domain_of:
- GlobalStatistics
range: SummaryStatisticCollection
inlined: true

```
</details>