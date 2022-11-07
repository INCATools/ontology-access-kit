# Slot: object_property_count

URI: [reporting:object_property_count](https://w3id.org/linkml/reportobject_property_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **object_property_count**





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
| filter | ObjectProperty |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: object_property_count
annotations:
  filter:
    tag: filter
    value: ObjectProperty
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: object_property_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: property_statistic_group
range: string

```
</details>