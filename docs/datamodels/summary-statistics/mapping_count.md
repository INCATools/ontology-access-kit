

# Slot: mapping_count


_Number of mappings (including xrefs) in the ontology or subset_





URI: [summary_statistics:mapping_count](https://w3id.org/oaklib/summary_statistics.mapping_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **mapping_count**






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
| filter | Mapping |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:mapping_count |
| native | summary_statistics:mapping_count |




## LinkML Source

<details>
```yaml
name: mapping_count
annotations:
  filter:
    tag: filter
    value: Mapping
description: Number of mappings (including xrefs) in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: mapping_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: metadata_statistic_group
range: integer

```
</details>