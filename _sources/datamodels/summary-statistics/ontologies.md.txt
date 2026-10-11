

# Slot: ontologies


_Ontology for which the statistics are computed_





URI: [summary_statistics:ontologies](https://w3id.org/oaklib/summary_statistics.ontologies)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GroupedStatistics](GroupedStatistics.md) | summary statistics for the entire resource |  no  |
| [SummaryStatisticsReport](SummaryStatisticsReport.md) | abstract base class for all summary statistics reports |  no  |
| [UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |  no  |







## Properties

* Range: [Ontology](Ontology.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:ontologies |
| native | summary_statistics:ontologies |




## LinkML Source

<details>
```yaml
name: ontologies
description: Ontology for which the statistics are computed
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
alias: ontologies
owner: SummaryStatisticsReport
domain_of:
- SummaryStatisticsReport
range: Ontology
multivalued: true
inlined: true
inlined_as_list: true

```
</details>