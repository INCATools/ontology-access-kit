

# Slot: annotation_property_count


_Number of annotation properties (metadata properties) in the ontology or subset_





URI: [summary_statistics:annotation_property_count](https://w3id.org/oaklib/summary_statistics.annotation_property_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **annotation_property_count**






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
| filter | AnnotationProperty |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:annotation_property_count |
| native | summary_statistics:annotation_property_count |




## LinkML Source

<details>
```yaml
name: annotation_property_count
annotations:
  filter:
    tag: filter
    value: AnnotationProperty
description: Number of annotation properties (metadata properties) in the ontology
  or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: annotation_property_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: property_statistic_group
range: integer

```
</details>