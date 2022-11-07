# Slot: anonymous_individual_count

URI: [reporting:anonymous_individual_count](https://w3id.org/linkml/reportanonymous_individual_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **anonymous_individual_count**





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
| filter | AnonymousIndividual |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: anonymous_individual_count
annotations:
  filter:
    tag: filter
    value: AnonymousIndividual
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: anonymous_individual_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: individual_statistic_group
range: string
equals_expression: '{named_individual_count} - {individual_count}'

```
</details>