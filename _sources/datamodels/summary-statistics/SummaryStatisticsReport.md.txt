

# Class: SummaryStatisticsReport


_abstract base class for all summary statistics reports_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [summary_statistics:SummaryStatisticsReport](https://w3id.org/oaklib/summary_statistics.SummaryStatisticsReport)






```{mermaid}
 classDiagram
    class SummaryStatisticsReport
    click SummaryStatisticsReport href "../SummaryStatisticsReport"
      SummaryStatisticsReport <|-- GroupedStatistics
        click GroupedStatistics href "../GroupedStatistics"
      SummaryStatisticsReport <|-- UngroupedStatistics
        click UngroupedStatistics href "../UngroupedStatistics"
      
      SummaryStatisticsReport : agents
        
          
    
    
    SummaryStatisticsReport --> "*" Agent : agents
    click Agent href "../Agent"

        
      SummaryStatisticsReport : compared_with
        
          
    
    
    SummaryStatisticsReport --> "*" Ontology : compared_with
    click Ontology href "../Ontology"

        
      SummaryStatisticsReport : id
        
      SummaryStatisticsReport : ontologies
        
          
    
    
    SummaryStatisticsReport --> "*" Ontology : ontologies
    click Ontology href "../Ontology"

        
      SummaryStatisticsReport : was_generated_by
        
          
    
    
    SummaryStatisticsReport --> "0..1" SummaryStatisticsCalculationActivity : was_generated_by
    click SummaryStatisticsCalculationActivity href "../SummaryStatisticsCalculationActivity"

        
      
```





## Inheritance
* **SummaryStatisticsReport**
    * [GroupedStatistics](GroupedStatistics.md)
    * [UngroupedStatistics](UngroupedStatistics.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [String](String.md) | Unique handle for this report | direct |
| [ontologies](ontologies.md) | * <br/> [Ontology](Ontology.md) | Ontology for which the statistics are computed | direct |
| [compared_with](compared_with.md) | * <br/> [Ontology](Ontology.md) | For diffs, the ontologies being compared against | direct |
| [was_generated_by](was_generated_by.md) | 0..1 <br/> [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) | The process that generated the report | direct |
| [agents](agents.md) | * <br/> [Agent](Agent.md) | Agents that contributed to the report | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




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
from_schema: https://w3id.org/oak/summary_statistics
abstract: true
attributes:
  id:
    name: id
    description: Unique handle for this report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - SummaryStatisticsReport
    - Ontology
    - Agent
    - ContributorRole
    required: true
  ontologies:
    name: ontologies
    description: Ontology for which the statistics are computed
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - SummaryStatisticsReport
    range: Ontology
    multivalued: true
    inlined: true
    inlined_as_list: true
  compared_with:
    name: compared_with
    description: For diffs, the ontologies being compared against
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - SummaryStatisticsReport
    range: Ontology
    multivalued: true
    inlined: true
    inlined_as_list: true
  was_generated_by:
    name: was_generated_by
    description: The process that generated the report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - SummaryStatisticsReport
    range: SummaryStatisticsCalculationActivity
  agents:
    name: agents
    description: Agents that contributed to the report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - SummaryStatisticsReport
    range: Agent
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>

### Induced

<details>
```yaml
name: SummaryStatisticsReport
description: abstract base class for all summary statistics reports
from_schema: https://w3id.org/oak/summary_statistics
abstract: true
attributes:
  id:
    name: id
    description: Unique handle for this report
    from_schema: https://w3id.org/oak/summary_statistics
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
  compared_with:
    name: compared_with
    description: For diffs, the ontologies being compared against
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: compared_with
    owner: SummaryStatisticsReport
    domain_of:
    - SummaryStatisticsReport
    range: Ontology
    multivalued: true
    inlined: true
    inlined_as_list: true
  was_generated_by:
    name: was_generated_by
    description: The process that generated the report
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: was_generated_by
    owner: SummaryStatisticsReport
    domain_of:
    - SummaryStatisticsReport
    range: SummaryStatisticsCalculationActivity
  agents:
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