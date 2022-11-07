# Slot: unsatisfiable_class_count

URI: [reporting:unsatisfiable_class_count](https://w3id.org/linkml/reportunsatisfiable_class_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **unsatisfiable_class_count**





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
| filter | Class, Unsatisfiable |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: unsatisfiable_class_count
annotations:
  filter:
    tag: filter
    value: Class, Unsatisfiable
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: unsatisfiable_class_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: class_statistic_group
range: string

```
</details>