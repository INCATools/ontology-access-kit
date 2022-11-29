# Slot: merged_class_count

URI: [reporting:merged_class_count](https://w3id.org/linkml/reportmerged_class_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **merged_class_count**





## Applicable Classes

| Name | Description |
| --- | --- |
[SummaryStatisticCollection](SummaryStatisticCollection.md) | A summary statistics report object






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)







## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Class, Deprecated, Merged |



### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics




## LinkML Source

<details>
```yaml
name: merged_class_count
annotations:
  filter:
    tag: filter
    value: Class, Deprecated, Merged
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
is_a: count_statistic
alias: merged_class_count
owner: SummaryStatisticCollection
domain_of:
- SummaryStatisticCollection
slot_group: class_statistic_group
range: string

```
</details>