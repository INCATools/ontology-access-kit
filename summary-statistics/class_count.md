# Slot: class_count
_Number of classes in the ontology or subset_


URI: [reporting:class_count](https://w3id.org/linkml/reportclass_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **class_count**





## Applicable Classes

| Name | Description |
| --- | --- |
[UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)







## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Class |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: class_count
annotations:
  filter:
    tag: filter
    value: Class
description: Number of classes in the ontology or subset
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: class_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: class_statistic_group
range: string

```
</details>