

# Slot: named_individual_count


_Number of named individuals in the ontology or subset_





URI: [summary_statistics:named_individual_count](https://w3id.org/oaklib/summary_statistics.named_individual_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **named_individual_count**






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
| filter | NamedIndividual |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:named_individual_count |
| native | summary_statistics:named_individual_count |




## LinkML Source

<details>
```yaml
name: named_individual_count
annotations:
  filter:
    tag: filter
    value: NamedIndividual
description: Number of named individuals in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: named_individual_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: individual_statistic_group
range: integer

```
</details>