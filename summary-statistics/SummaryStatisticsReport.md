# Class: SummaryStatisticsReport
_abstract base class for all summary statistics reports_



* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [summary_statistics:SummaryStatisticsReport](https://w3id.org/oaklib/summary_statistics.SummaryStatisticsReport)



```{mermaid}
 classDiagram
    class SummaryStatisticsReport
      SummaryStatisticsReport <|-- GroupedStatistics
      SummaryStatisticsReport <|-- UngroupedStatistics
      
      SummaryStatisticsReport : agents
        
          SummaryStatisticsReport ..> Agent : agents
        
      SummaryStatisticsReport : compared_with
        
          SummaryStatisticsReport ..> Ontology : compared_with
        
      SummaryStatisticsReport : id
        
      SummaryStatisticsReport : ontologies
        
          SummaryStatisticsReport ..> Ontology : ontologies
        
      SummaryStatisticsReport : was_generated_by
        
          SummaryStatisticsReport ..> SummaryStatisticsCalculationActivity : was_generated_by
        
      
```





## Inheritance
* **SummaryStatisticsReport**
    * [GroupedStatistics](GroupedStatistics.md)
    * [UngroupedStatistics](UngroupedStatistics.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 0..1 <br/> [String](String.md) |  | direct |
| [ontologies](ontologies.md) | 0..* <br/> [Ontology](Ontology.md) | Ontology for which the statistics are computed | direct |
| [compared_with](compared_with.md) | 0..* <br/> [Ontology](Ontology.md) | For diffs, the ontologies being compared against | direct |
| [was_generated_by](was_generated_by.md) | 0..1 <br/> [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) | The process that generated the report | direct |
| [agents](agents.md) | 0..* <br/> [Agent](Agent.md) | Agents that contributed to the report | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oaklib/summary_statistics





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:SummaryStatisticsReport |
| native | summary_statistics:SummaryStatisticsReport |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SummaryStatisticsReport
description: abstract base class for all summary statistics reports
from_schema: https://w3id.org/oaklib/summary_statistics
rank: 1000
abstract: true
attributes:
  id:
    name: id
    description: Unique handle for this report
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    required: true
  ontologies:
    name: ontologies
    description: Ontology for which the statistics are computed
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    multivalued: true
    range: Ontology
    inlined: true
    inlined_as_list: true
  compared_with:
    name: compared_with
    description: For diffs, the ontologies being compared against
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    multivalued: true
    range: Ontology
    inlined: true
    inlined_as_list: true
  was_generated_by:
    name: was_generated_by
    description: The process that generated the report
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    range: SummaryStatisticsCalculationActivity
  agents:
    name: agents
    description: Agents that contributed to the report
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    multivalued: true
    range: Agent
    inlined: true
    inlined_as_list: true

```
</details>

### Induced

<details>
```yaml
name: SummaryStatisticsReport
description: abstract base class for all summary statistics reports
from_schema: https://w3id.org/oaklib/summary_statistics
rank: 1000
abstract: true
attributes:
  id:
    name: id
    description: Unique handle for this report
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    alias: id
    owner: SummaryStatisticsReport
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
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    multivalued: true
    alias: ontologies
    owner: SummaryStatisticsReport
    domain_of:
    - SummaryStatisticsReport
    range: Ontology
    inlined: true
    inlined_as_list: true
  compared_with:
    name: compared_with
    description: For diffs, the ontologies being compared against
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    multivalued: true
    alias: compared_with
    owner: SummaryStatisticsReport
    domain_of:
    - SummaryStatisticsReport
    range: Ontology
    inlined: true
    inlined_as_list: true
  was_generated_by:
    name: was_generated_by
    description: The process that generated the report
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    alias: was_generated_by
    owner: SummaryStatisticsReport
    domain_of:
    - SummaryStatisticsReport
    range: SummaryStatisticsCalculationActivity
  agents:
    name: agents
    description: Agents that contributed to the report
    from_schema: https://w3id.org/oaklib/summary_statistics
    rank: 1000
    multivalued: true
    alias: agents
    owner: SummaryStatisticsReport
    domain_of:
    - SummaryStatisticsReport
    range: Agent
    inlined: true
    inlined_as_list: true

```
</details>