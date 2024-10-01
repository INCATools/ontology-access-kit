

# Slot: synonym_statement_count


_Number of synonym statements (assertions) in the ontology or subset_





URI: [summary_statistics:synonym_statement_count](https://w3id.org/oaklib/summary_statistics.synonym_statement_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **synonym_statement_count**






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
| filter | Synonym |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:synonym_statement_count |
| native | summary_statistics:synonym_statement_count |




## LinkML Source

<details>
```yaml
name: synonym_statement_count
annotations:
  filter:
    tag: filter
    value: Synonym
description: Number of synonym statements (assertions) in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: synonym_statement_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: metadata_statistic_group
range: integer

```
</details>