

# Slot: synonym_statement_count_by_predicate


_Number of synonym statements (assertions) grouped by predicate (scope) in the ontology or subset_





URI: [summary_statistics:synonym_statement_count_by_predicate](https://w3id.org/oaklib/summary_statistics.synonym_statement_count_by_predicate)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |  no  |







## Properties

* Range: [FacetedCount](FacetedCount.md)

* Multivalued: True





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| filter | Synonym || facet | Predicate |



### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:synonym_statement_count_by_predicate |
| native | summary_statistics:synonym_statement_count_by_predicate |




## LinkML Source

<details>
```yaml
name: synonym_statement_count_by_predicate
annotations:
  filter:
    tag: filter
    value: Synonym
  facet:
    tag: facet
    value: Predicate
description: Number of synonym statements (assertions) grouped by predicate (scope)
  in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
alias: synonym_statement_count_by_predicate
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: metadata_statistic_group
range: FacetedCount
multivalued: true
inlined: true

```
</details>