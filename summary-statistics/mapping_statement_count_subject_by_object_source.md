

# Slot: mapping_statement_count_subject_by_object_source


_Number of distinct subject entities grouped by object_source (prefix of external vocabulary) in the ontology or subset_





URI: [summary_statistics:mapping_statement_count_subject_by_object_source](https://w3id.org/oaklib/summary_statistics.mapping_statement_count_subject_by_object_source)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |  no  |







## Properties

* Range: [FacetedCount](FacetedCount.md)

* Multivalued: True





## Comments

* for exact or one-to-one mappings this should generally be the same as mapping_statement_count_by_object_source

## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Mapping || facet | ObjectSource || distinct | Subject |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:mapping_statement_count_subject_by_object_source |
| native | summary_statistics:mapping_statement_count_subject_by_object_source |




## LinkML Source

<details>
```yaml
name: mapping_statement_count_subject_by_object_source
annotations:
  filter:
    tag: filter
    value: Mapping
  facet:
    tag: facet
    value: ObjectSource
  distinct:
    tag: distinct
    value: Subject
description: Number of distinct subject entities grouped by object_source (prefix
  of external vocabulary) in the ontology or subset
comments:
- for exact or one-to-one mappings this should generally be the same as mapping_statement_count_by_object_source
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
alias: mapping_statement_count_subject_by_object_source
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: metadata_statistic_group
range: FacetedCount
multivalued: true
inlined: true

```
</details>