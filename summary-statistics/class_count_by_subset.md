# Slot: class_count_by_subset

URI: [reporting:class_count_by_subset](https://w3id.org/linkml/reportclass_count_by_subset)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[SummaryStatisticCollection](SummaryStatisticCollection.md) | A summary statistics report object






## Properties

* Range: [FacetedCount](FacetedCount.md)
* Multivalued: True








## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Subset || facet | Predicate |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: class_count_by_subset
annotations:
  filter:
    tag: filter
    value: Subset
  facet:
    tag: facet
    value: Predicate
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
multivalued: true
alias: class_count_by_subset
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: metadata_statistic_group
range: FacetedCount
inlined: true

```
</details>