

# Slot: was_associated_with


_the agent that was associated with the activity_





URI: [prov:wasAssociatedWith](http://www.w3.org/ns/prov#wasAssociatedWith)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) | An activity that calculates summary statistics for an ontology |  no  |







## Properties

* Range: [Agent](Agent.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | prov:wasAssociatedWith |
| native | summary_statistics:was_associated_with |




## LinkML Source

<details>
```yaml
name: was_associated_with
description: the agent that was associated with the activity
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
slot_uri: prov:wasAssociatedWith
alias: was_associated_with
owner: SummaryStatisticsCalculationActivity
domain_of:
- SummaryStatisticsCalculationActivity
range: Agent

```
</details>