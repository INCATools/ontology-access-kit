# Slot: ontology_count

URI: [reporting:ontology_count](https://w3id.org/linkml/reportontology_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **ontology_count**





## Applicable Classes

| Name | Description |
| --- | --- |
[SummaryStatisticCollection](SummaryStatisticCollection.md) | A summary statistics report object
[GlobalStatistics](GlobalStatistics.md) | summary statistics for the entire resource
[FacetStatistics](FacetStatistics.md) | summary statistics for a data facet






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)
* Multivalued: None







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: ontology_count
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: ontology_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
range: string

```
</details>