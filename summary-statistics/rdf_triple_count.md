# Slot: rdf_triple_count

URI: [reporting:rdf_triple_count](https://w3id.org/linkml/reportrdf_triple_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **rdf_triple_count**





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







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: rdf_triple_count
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: rdf_triple_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: owl_statistic_group
range: string

```
</details>