# Class: GroupedStatistics
_summary statistics for the entire resource_




URI: [summary_statistics:GroupedStatistics](https://w3id.org/oaklib/summary_statistics.GroupedStatistics)



```{mermaid}
 classDiagram
    class GroupedStatistics
      SummaryStatisticsReport <|-- GroupedStatistics
      
      GroupedStatistics : agents
        
          GroupedStatistics ..> Agent : agents
        
      GroupedStatistics : compared_with
        
          GroupedStatistics ..> Ontology : compared_with
        
      GroupedStatistics : id
        
      GroupedStatistics : ontologies
        
          GroupedStatistics ..> Ontology : ontologies
        
      GroupedStatistics : partitions
        
          GroupedStatistics ..> UngroupedStatistics : partitions
        
      GroupedStatistics : was_generated_by
        
          GroupedStatistics ..> SummaryStatisticsCalculationActivity : was_generated_by
        
      
```





## Inheritance
* [SummaryStatisticsReport](SummaryStatisticsReport.md)
    * **GroupedStatistics**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [partitions](partitions.md) | 0..* <br/> [UngroupedStatistics](UngroupedStatistics.md) | statistics grouped by a particular property | direct |
| [id](id.md) | 1..1 <br/> [String](String.md) | Unique handle for this report | [SummaryStatisticsReport](SummaryStatisticsReport.md) |
| [ontologies](ontologies.md) | 0..* <br/> [Ontology](Ontology.md) | Ontology for which the statistics are computed | [SummaryStatisticsReport](SummaryStatisticsReport.md) |
| [compared_with](compared_with.md) | 0..* <br/> [Ontology](Ontology.md) | For diffs, the ontologies being compared against | [SummaryStatisticsReport](SummaryStatisticsReport.md) |
| [was_generated_by](was_generated_by.md) | 0..1 <br/> [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) | The process that generated the report | [SummaryStatisticsReport](SummaryStatisticsReport.md) |
| [agents](agents.md) | 0..* <br/> [Agent](Agent.md) | Agents that contributed to the report | [SummaryStatisticsReport](SummaryStatisticsReport.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:GroupedStatistics |
| native | summary_statistics:GroupedStatistics |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: GroupedStatistics
description: summary statistics for the entire resource
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: SummaryStatisticsReport
attributes:
  partitions:
    name: partitions
    description: statistics grouped by a particular property
    comments:
    - For example, GO stats may be broken out by MF/BP/CC
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    multivalued: true
    range: UngroupedStatistics
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: GroupedStatistics
description: summary statistics for the entire resource
from_schema: https://w3id.org/oak/summary_statistics
rank: 1000
is_a: SummaryStatisticsReport
attributes:
  partitions:
    name: partitions
    description: statistics grouped by a particular property
    comments:
    - For example, GO stats may be broken out by MF/BP/CC
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    multivalued: true
    alias: partitions
    owner: GroupedStatistics
    domain_of:
    - GroupedStatistics
    range: UngroupedStatistics
    inlined: true
  id:
    name: id
    description: Unique handle for this report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: id
    owner: GroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    - Ontology
    - Agent
    - ContributorRole
    range: string
    required: true
  ontologies:
    name: ontologies
    description: Ontology for which the statistics are computed
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    multivalued: true
    alias: ontologies
    owner: GroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    range: Ontology
    inlined: true
    inlined_as_list: true
  compared_with:
    name: compared_with
    description: For diffs, the ontologies being compared against
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    multivalued: true
    alias: compared_with
    owner: GroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    range: Ontology
    inlined: true
    inlined_as_list: true
  was_generated_by:
    name: was_generated_by
    description: The process that generated the report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: was_generated_by
    owner: GroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    range: SummaryStatisticsCalculationActivity
  agents:
    name: agents
    description: Agents that contributed to the report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    multivalued: true
    alias: agents
    owner: GroupedStatistics
    domain_of:
    - SummaryStatisticsReport
    range: Agent
    inlined: true
    inlined_as_list: true

```
</details>