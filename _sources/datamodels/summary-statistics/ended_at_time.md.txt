

# Slot: ended_at_time


_the time at which the activity ended_





URI: [prov:endedAtTime](http://www.w3.org/ns/prov#endedAtTime)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) | An activity that calculates summary statistics for an ontology |  no  |







## Properties

* Range: [Datetime](Datetime.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | prov:endedAtTime |
| native | summary_statistics:ended_at_time |




## LinkML Source

<details>
```yaml
name: ended_at_time
description: the time at which the activity ended
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
slot_uri: prov:endedAtTime
alias: ended_at_time
owner: SummaryStatisticsCalculationActivity
domain_of:
- SummaryStatisticsCalculationActivity
range: datetime

```
</details>