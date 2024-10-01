

# Slot: class_count_by_category


_Number of classes grouped by category in the ontology or subset_





URI: [summary_statistics:class_count_by_category](https://w3id.org/oaklib/summary_statistics.class_count_by_category)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |  no  |







## Properties

* Range: [FacetedCount](FacetedCount.md)

* Multivalued: True





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Class || facet | Category |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:class_count_by_category |
| native | summary_statistics:class_count_by_category |




## LinkML Source

<details>
```yaml
name: class_count_by_category
annotations:
  filter:
    tag: filter
    value: Class
  facet:
    tag: facet
    value: Category
description: Number of classes grouped by category in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
alias: class_count_by_category
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: metadata_statistic_group
range: FacetedCount
multivalued: true
inlined: true

```
</details>