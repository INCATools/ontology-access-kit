

# Slot: rdf_triple_count


_Number of RDF triples in the ontology or subset_





URI: [summary_statistics:rdf_triple_count](https://w3id.org/oaklib/summary_statistics.rdf_triple_count)




## Inheritance

* [count_statistic](count_statistic.md)
    * **rdf_triple_count**






## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |  no  |







## Properties

* Range: [Integer](Integer.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:rdf_triple_count |
| native | summary_statistics:rdf_triple_count |




## LinkML Source

<details>
```yaml
name: rdf_triple_count
description: Number of RDF triples in the ontology or subset
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: count_statistic
alias: rdf_triple_count
owner: UngroupedStatistics
domain_of:
- UngroupedStatistics
slot_group: owl_statistic_group
range: integer

```
</details>