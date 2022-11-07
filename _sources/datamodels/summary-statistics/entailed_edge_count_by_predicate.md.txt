# Slot: entailed_edge_count_by_predicate

URI: [reporting:entailed_edge_count_by_predicate](https://w3id.org/linkml/reportentailed_edge_count_by_predicate)



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
| filter | EntailedEdge || facet | Predicate |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: entailed_edge_count_by_predicate
annotations:
  filter:
    tag: filter
    value: EntailedEdge
  facet:
    tag: facet
    value: Predicate
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
multivalued: true
alias: entailed_edge_count_by_predicate
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: metadata_statistic_group
range: FacetedCount
inlined: true

```
</details>