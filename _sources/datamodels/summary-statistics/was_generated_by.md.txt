

# Slot: was_generated_by


_The process that generated the report_





URI: [summary_statistics:was_generated_by](https://w3id.org/oaklib/summary_statistics.was_generated_by)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [GroupedStatistics](GroupedStatistics.md) | summary statistics for the entire resource |  no  |
| [UngroupedStatistics](UngroupedStatistics.md) | A summary statistics report object |  no  |
| [SummaryStatisticsReport](SummaryStatisticsReport.md) | abstract base class for all summary statistics reports |  no  |







## Properties

* Range: [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:was_generated_by |
| native | summary_statistics:was_generated_by |




## LinkML Source

<details>
```yaml
name: was_generated_by
description: The process that generated the report
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
alias: was_generated_by
owner: SummaryStatisticsReport
domain_of:
- SummaryStatisticsReport
range: SummaryStatisticsCalculationActivity

```
</details>