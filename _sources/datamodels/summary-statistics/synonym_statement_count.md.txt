# Slot: synonym_statement_count

URI: [reporting:synonym_statement_count](https://w3id.org/linkml/reportsynonym_statement_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **synonym_statement_count**





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
| filter | Synonym |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: synonym_statement_count
annotations:
  filter:
    tag: filter
    value: Synonym
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: synonym_statement_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: metadata_statistic_group
range: string

```
</details>