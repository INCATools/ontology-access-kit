

# Slot: individual_count


_Number of individuals (named and anonymous) in the ontology or subset_





URI: [summary_statistics:individual_count](https://w3id.org/oaklib/summary_statistics.individual_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **individual_count**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |  no  |







## Properties

* Range: [Integer](Integer.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Individual |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:individual_count |
| native | summary_statistics:individual_count |




## LinkML Source

<details>
```yaml
name: individual_count
annotations:
  filter:
    tag: filter
    value: Individual
description: Number of individuals (named and anonymous) in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: individual_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: individual_statistic_group
range: integer

```
</details>