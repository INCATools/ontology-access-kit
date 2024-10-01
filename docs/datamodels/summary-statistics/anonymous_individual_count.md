

# Slot: anonymous_individual_count


_Number of anonymous individuals in the ontology or subset_





URI: [summary_statistics:anonymous_individual_count](https://w3id.org/oaklib/summary_statistics.anonymous_individual_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **anonymous_individual_count**






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
| filter | AnonymousIndividual |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:anonymous_individual_count |
| native | summary_statistics:anonymous_individual_count |




## LinkML Source

<details>
```yaml
name: anonymous_individual_count
annotations:
  filter:
    tag: filter
    value: AnonymousIndividual
description: Number of anonymous individuals in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: anonymous_individual_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: individual_statistic_group
range: integer
equals_expression: '{named_individual_count} - {individual_count}'

```
</details>