# Slot: owl_axiom_count

URI: [reporting:owl_axiom_count](https://w3id.org/linkml/reportowl_axiom_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **owl_axiom_count**





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
| filter | Axiom |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: owl_axiom_count
annotations:
  filter:
    tag: filter
    value: Axiom
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: owl_axiom_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: owl_statistic_group
range: string

```
</details>