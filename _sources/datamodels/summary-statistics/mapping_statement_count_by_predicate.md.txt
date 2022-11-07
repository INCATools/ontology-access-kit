# Slot: mapping_statement_count_by_predicate

URI: [reporting:mapping_statement_count_by_predicate](https://w3id.org/linkml/reportmapping_statement_count_by_predicate)



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
| filter | Mapping || facet | Predicate |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: mapping_statement_count_by_predicate
annotations:
  filter:
    tag: filter
    value: Mapping
  facet:
    tag: facet
    value: Predicate
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
multivalued: true
alias: mapping_statement_count_by_predicate
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: metadata_statistic_group
range: FacetedCount
inlined: true

```
</details>