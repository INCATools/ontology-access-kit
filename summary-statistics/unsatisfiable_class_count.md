# Slot: unsatisfiable_class_count
_Number of unsatisfiable classes in the ontology or subset_


URI: [summary_statistics:unsatisfiable_class_count](https://w3id.org/oaklib/summary_statistics.unsatisfiable_class_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **unsatisfiable_class_count**





## Applicable Classes

| Name | Description |
| --- | --- |
[UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object






## Properties

* Range: [Integer](Integer.md)







## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Class, Unsatisfiable |



### Schema Source


* from schema: https://w3id.org/oaklib/summary_statistics




## LinkML Source

<details>
```yaml
name: unsatisfiable_class_count
annotations:
  filter:
    tag: filter
    value: Class, Unsatisfiable
description: Number of unsatisfiable classes in the ontology or subset
from_schema: https://w3id.org/oaklib/summary_statistics
rank: 1000
is_a: count_statistic
alias: unsatisfiable_class_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: class_statistic_group
range: integer

```
</details>