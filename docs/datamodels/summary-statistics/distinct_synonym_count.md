

# Slot: distinct_synonym_count


_Number of distinct synonym strings in the ontology or subset_





URI: [summary_statistics:distinct_synonym_count](https://w3id.org/oaklib/summary_statistics.distinct_synonym_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **distinct_synonym_count**






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
| filter | Synonym || distinct | Value |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:distinct_synonym_count |
| native | summary_statistics:distinct_synonym_count |




## LinkML Source

<details>
```yaml
name: distinct_synonym_count
annotations:
  filter:
    tag: filter
    value: Synonym
  distinct:
    tag: distinct
    value: Value
description: Number of distinct synonym strings in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: distinct_synonym_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: metadata_statistic_group
range: integer

```
</details>