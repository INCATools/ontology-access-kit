

# Slot: deprecated_object_property_count


_Number of deprecated (obsoleted) object properties in the ontology or subset_





URI: [summary_statistics:deprecated_object_property_count](https://w3id.org/oaklib/summary_statistics.deprecated_object_property_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **deprecated_object_property_count**






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
| filter | ObjectProperty, Deprecated |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:deprecated_object_property_count |
| native | summary_statistics:deprecated_object_property_count |




## LinkML Source

<details>
```yaml
name: deprecated_object_property_count
annotations:
  filter:
    tag: filter
    value: ObjectProperty, Deprecated
description: Number of deprecated (obsoleted) object properties in the ontology or
  subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: deprecated_object_property_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: property_statistic_group
range: integer

```
</details>