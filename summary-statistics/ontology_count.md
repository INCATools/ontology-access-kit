# Slot: ontology_count
_Number of ontologies (including imports) for the ontology or subset_


URI: [summary_statistics:ontology_count](https://w3id.org/oaklib/summary_statistics.ontology_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **ontology_count**





## Applicable Classes

| Name | Description |
| --- | --- |
[UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object






## Properties

* Range: [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)







## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Ontology |



### Schema Source


* from schema: https://w3id.org/oaklib/summary_statistics




## LinkML Source

<details>
```yaml
name: ontology_count
annotations:
  filter:
    tag: filter
    value: Ontology
description: Number of ontologies (including imports) for the ontology or subset
from_schema: https://w3id.org/oaklib/summary_statistics
rank: 1000
is_a: count_statistic
alias: ontology_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
range: integer

```
</details>