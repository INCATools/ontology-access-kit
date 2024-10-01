

# Slot: started_at_time


_the time at which the activity started_





URI: [prov:startedAtTime](http://www.w3.org/ns/prov#startedAtTime)



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
| self | prov:startedAtTime |
| native | summary_statistics:started_at_time |




## LinkML Source

<details>
```yaml
name: started_at_time
description: the time at which the activity started
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
slot_uri: prov:startedAtTime
alias: started_at_time
owner: SummaryStatisticsCalculationActivity
domain_of:
- SummaryStatisticsCalculationActivity
range: datetime

```
</details>