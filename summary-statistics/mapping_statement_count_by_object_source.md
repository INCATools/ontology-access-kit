# Slot: mapping_statement_count_by_object_source
_Number of mappings grouped by object_source (prefix of external vocabulary) in the ontology or subset_


URI: [summary_statistics:mapping_statement_count_by_object_source](https://w3id.org/oaklib/summary_statistics.mapping_statement_count_by_object_source)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object






## Properties

* Range: [FacetedCount](FacetedCount.md)
* Multivalued: True








## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Mapping || facet | ObjectSource |



### Schema Source


* from schema: https://w3id.org/oaklib/summary_statistics




## LinkML Source

<details>
```yaml
name: mapping_statement_count_by_object_source
annotations:
  filter:
    tag: filter
    value: Mapping
  facet:
    tag: facet
    value: ObjectSource
description: Number of mappings grouped by object_source (prefix of external vocabulary)
  in the ontology or subset
from_schema: https://w3id.org/oaklib/summary_statistics
rank: 1000
multivalued: true
alias: mapping_statement_count_by_object_source
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: metadata_statistic_group
range: FacetedCount
inlined: true

```
</details>