

# Slot: agents


_Agents that contributed to the report_





URI: [summary_statistics:agents](https://w3id.org/oaklib/summary_statistics.agents)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GroupedStatistics](GroupedStatistics.md) | summary statistics for the entire resource |  no  |
| [SummaryStatisticsReport](SummaryStatisticsReport.md) | abstract base class for all summary statistics reports |  no  |
| [UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |  no  |







## Properties

* Range: [Agent](Agent.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:agents |
| native | summary_statistics:agents |




## LinkML Source

<details>
```yaml
name: agents
description: Agents that contributed to the report
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
alias: agents
owner: SummaryStatisticsReport
domain_of:
- SummaryStatisticsReport
range: Agent
multivalued: true
inlined: true
inlined_as_list: true

```
</details>