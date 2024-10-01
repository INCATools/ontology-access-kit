

# Slot: acted_on_behalf_of


_the agent that the activity acted on behalf of_





URI: [prov:actedOnBehalfOf](http://www.w3.org/ns/prov#actedOnBehalfOf)



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
| self | prov:actedOnBehalfOf |
| native | summary_statistics:acted_on_behalf_of |




## LinkML Source

<details>
```yaml
name: acted_on_behalf_of
description: the agent that the activity acted on behalf of
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
slot_uri: prov:actedOnBehalfOf
alias: acted_on_behalf_of
owner: SummaryStatisticsCalculationActivity
domain_of:
- SummaryStatisticsCalculationActivity
range: Agent

```
</details>