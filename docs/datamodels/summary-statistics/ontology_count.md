

# Slot: ontology_count


_Number of ontologies (including imports) for the ontology or subset_





URI: [summary_statistics:ontology_count](https://w3id.org/oaklib/summary_statistics.ontology_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **ontology_count**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |  no  |







## Properties

* Range: [Integer](Integer.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Ontology |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:ontology_count |
| native | summary_statistics:ontology_count |




## LinkML Source

<details>
```yaml
name: ontology_count
annotations:
  filter:
    tag: filter
    value: Ontology
description: Number of ontologies (including imports) for the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: ontology_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
range: integer

```
</details>