

# Slot: class_count


_Number of classes in the ontology or subset_





URI: [summary_statistics:class_count](https://w3id.org/oaklib/summary_statistics.class_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **class_count**






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
| filter | Class |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:class_count |
| native | summary_statistics:class_count |




## LinkML Source

<details>
```yaml
name: class_count
annotations:
  filter:
    tag: filter
    value: Class
description: Number of classes in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: class_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: class_statistic_group
range: integer

```
</details>