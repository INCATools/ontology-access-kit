# Slot: class_count_by_category

URI: [reporting:class_count_by_category](https://w3id.org/linkml/reportclass_count_by_category)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[SummaryStatisticCollection](SummaryStatisticCollection.md) | A summary statistics report object
[GlobalStatistics](GlobalStatistics.md) | summary statistics for the entire resource
[FacetStatistics](FacetStatistics.md) | summary statistics for a data facet






## Properties

* Range: [FacetedCount](FacetedCount.md)
* Multivalued: True







## Alias




## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Class || facet | Category |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




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
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
multivalued: true
alias: class_count_by_category
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: metadata_statistic_group
range: FacetedCount
inlined: true

```
</details>