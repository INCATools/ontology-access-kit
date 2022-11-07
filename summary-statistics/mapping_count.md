# Slot: mapping_count

URI: [reporting:mapping_count](https://w3id.org/linkml/reportmapping_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **mapping_count**





## Applicable Classes

| Name | Description |
| --- | --- |
[SummaryStatisticCollection](SummaryStatisticCollection.md) | A summary statistics report object
[GlobalStatistics](GlobalStatistics.md) | summary statistics for the entire resource
[FacetStatistics](FacetStatistics.md) | summary statistics for a data facet






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)






## Alias




## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Mapping |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: mapping_count
annotations:
  filter:
    tag: filter
    value: Mapping
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: mapping_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: metadata_statistic_group
range: string

```
</details>