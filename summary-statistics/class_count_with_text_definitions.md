

# Slot: class_count_with_text_definitions


_Number of classes with text definitions in the ontology or subset_





URI: [summary_statistics:class_count_with_text_definitions](https://w3id.org/oaklib/summary_statistics.class_count_with_text_definitions)




## Inheritance

* [count_statistic](count_statistic.md)
    * **class_count_with_text_definitions**






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
| filter | Class, HasTextDefinition |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:class_count_with_text_definitions |
| native | summary_statistics:class_count_with_text_definitions |




## LinkML Source

<details>
```yaml
name: class_count_with_text_definitions
annotations:
  filter:
    tag: filter
    value: Class, HasTextDefinition
description: Number of classes with text definitions in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: class_count_with_text_definitions
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: class_statistic_group
range: integer

```
</details>