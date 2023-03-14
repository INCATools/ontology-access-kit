# Class: SummaryStatisticsCalculationActivity
_An activity that calculates summary statistics for an ontology_




URI: [summary_statistics:SummaryStatisticsCalculationActivity](https://w3id.org/oaklib/summary_statistics.SummaryStatisticsCalculationActivity)



```{mermaid}
 classDiagram
    class SummaryStatisticsCalculationActivity
      SummaryStatisticsCalculationActivity : acted_on_behalf_of
        
          SummaryStatisticsCalculationActivity ..> Agent : acted_on_behalf_of
        
      SummaryStatisticsCalculationActivity : ended_at_time
        
      SummaryStatisticsCalculationActivity : started_at_time
        
      SummaryStatisticsCalculationActivity : was_associated_with
        
          SummaryStatisticsCalculationActivity ..> Agent : was_associated_with
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [started_at_time](started_at_time.md) | 0..1 <br/> [Datetime](Datetime.md) | the time at which the activity started | direct |
| [ended_at_time](ended_at_time.md) | 0..1 <br/> [Datetime](Datetime.md) | the time at which the activity ended | direct |
| [was_associated_with](was_associated_with.md) | 0..1 <br/> [Agent](Agent.md) | the agent that was associated with the activity | direct |
| [acted_on_behalf_of](acted_on_behalf_of.md) | 0..1 <br/> [Agent](Agent.md) | the agent that the activity acted on behalf of | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SummaryStatisticsReport](SummaryStatisticsReport.md) | [was_generated_by](was_generated_by.md) | range | [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) |
| [GroupedStatistics](GroupedStatistics.md) | [was_generated_by](was_generated_by.md) | range | [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) |
| [UngroupedStatistics](UngroupedStatistics.md) | [was_generated_by](was_generated_by.md) | range | [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oaklib/summary_statistics





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:SummaryStatisticsCalculationActivity |
| native | summary_statistics:SummaryStatisticsCalculationActivity |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SummaryStatisticsCalculationActivity
description: An activity that calculates summary statistics for an ontology
from_schema: https://w3id.org/oaklib/summary_statistics
rank: 1000
attributes:
  started_at_time:
    name: started_at_time
    description: the time at which the activity started
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    slot_uri: prov:startedAtTime
    range: datetime
  ended_at_time:
    name: ended_at_time
    description: the time at which the activity ended
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    slot_uri: prov:endedAtTime
    range: datetime
  was_associated_with:
    name: was_associated_with
    description: the agent that was associated with the activity
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    slot_uri: prov:wasAssociatedWith
    range: Agent
  acted_on_behalf_of:
    name: acted_on_behalf_of
    description: the agent that the activity acted on behalf of
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    slot_uri: prov:actedOnBehalfOf
    range: Agent

```
</details>

### Induced

<details>
```yaml
name: SummaryStatisticsCalculationActivity
description: An activity that calculates summary statistics for an ontology
from_schema: https://w3id.org/oaklib/summary_statistics
rank: 1000
attributes:
  started_at_time:
    name: started_at_time
    description: the time at which the activity started
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    slot_uri: prov:startedAtTime
    alias: started_at_time
    owner: SummaryStatisticsCalculationActivity
    domain_of:
    - SummaryStatisticsCalculationActivity
    range: datetime
  ended_at_time:
    name: ended_at_time
    description: the time at which the activity ended
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    slot_uri: prov:endedAtTime
    alias: ended_at_time
    owner: SummaryStatisticsCalculationActivity
    domain_of:
    - SummaryStatisticsCalculationActivity
    range: datetime
  was_associated_with:
    name: was_associated_with
    description: the agent that was associated with the activity
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    slot_uri: prov:wasAssociatedWith
    alias: was_associated_with
    owner: SummaryStatisticsCalculationActivity
    domain_of:
    - SummaryStatisticsCalculationActivity
    range: Agent
  acted_on_behalf_of:
    name: acted_on_behalf_of
    description: the agent that the activity acted on behalf of
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    slot_uri: prov:actedOnBehalfOf
    alias: acted_on_behalf_of
    owner: SummaryStatisticsCalculationActivity
    domain_of:
    - SummaryStatisticsCalculationActivity
    range: Agent

```
</details>