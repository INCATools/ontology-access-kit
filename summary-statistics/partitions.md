

# Slot: partitions


_statistics grouped by a particular property_





URI: [summary_statistics:partitions](https://w3id.org/oaklib/summary_statistics.partitions)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GroupedStatistics](GroupedStatistics.md) | summary statistics for the entire resource |  no  |







## Properties

* Range: [UngroupedStatistics](UngroupedStatistics.md)

* Multivalued: True





## Comments

* For example, GO stats may be broken out by MF/BP/CC

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:partitions |
| native | summary_statistics:partitions |




## LinkML Source

<details>
```yaml
name: partitions
description: statistics grouped by a particular property
comments:
- For example, GO stats may be broken out by MF/BP/CC
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
alias: partitions
owner: GroupedStatistics
domain_of:
- GroupedStatistics
range: UngroupedStatistics
multivalued: true
inlined: true

```
</details>