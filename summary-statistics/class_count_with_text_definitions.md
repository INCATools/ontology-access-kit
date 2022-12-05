# Slot: class_count_with_text_definitions
_Number of classes with text definitions in the ontology or subset_


URI: [reporting:class_count_with_text_definitions](https://w3id.org/linkml/reportclass_count_with_text_definitions)




## Inheritance

* [count_statistic](count_statistic.md)
    * **class_count_with_text_definitions**





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
| filter | Class, HasTextDefinition |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: class_count_with_text_definitions
annotations:
  filter:
    tag: filter
    value: Class, HasTextDefinition
description: Number of classes with text definitions in the ontology or subset
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: class_count_with_text_definitions
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: class_statistic_group
range: string

```
</details>