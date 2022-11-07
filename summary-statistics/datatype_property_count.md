# Slot: datatype_property_count

URI: [reporting:datatype_property_count](https://w3id.org/linkml/reportdatatype_property_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **datatype_property_count**





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
| filter | DatatypeProperty |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: datatype_property_count
annotations:
  filter:
    tag: filter
    value: DatatypeProperty
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: datatype_property_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: property_statistic_group
range: string

```
</details>