

# Class: Agent


_An agent_





URI: [prov:Agent](http://www.w3.org/ns/prov#Agent)






```{mermaid}
 classDiagram
    class Agent
    click Agent href "../Agent"
      Agent : id
        
      Agent : label
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [String](String.md) | the unique identifier for the agent | direct |
| [label](label.md) | 0..1 <br/> [String](String.md) | the label for the agent | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SummaryStatisticsReport](SummaryStatisticsReport.md) | [agents](agents.md) | range | [Agent](Agent.md) |
| [GroupedStatistics](GroupedStatistics.md) | [agents](agents.md) | range | [Agent](Agent.md) |
| [UngroupedStatistics](UngroupedStatistics.md) | [agents](agents.md) | range | [Agent](Agent.md) |
| [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) | [was_associated_with](was_associated_with.md) | range | [Agent](Agent.md) |
| [SummaryStatisticsCalculationActivity](SummaryStatisticsCalculationActivity.md) | [acted_on_behalf_of](acted_on_behalf_of.md) | range | [Agent](Agent.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | prov:Agent |
| native | summary_statistics:Agent |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Agent
description: An agent
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  id:
    name: id
    description: the unique identifier for the agent
    from_schema: https://w3id.org/oak/summary_statistics
    identifier: true
    domain_of:
    - SummaryStatisticsReport
    - Ontology
    - Agent
    - ContributorRole
    range: string
    required: true
  label:
    name: label
    description: the label for the agent
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    slot_uri: rdfs:label
    domain_of:
    - Agent
    range: string
class_uri: prov:Agent

```
</details>

### Induced

<details>
```yaml
name: Agent
description: An agent
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  id:
    name: id
    description: the unique identifier for the agent
    from_schema: https://w3id.org/oak/summary_statistics
    identifier: true
    alias: id
    owner: Agent
    domain_of:
    - SummaryStatisticsReport
    - Ontology
    - Agent
    - ContributorRole
    range: string
    required: true
  label:
    name: label
    description: the label for the agent
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    slot_uri: rdfs:label
    alias: label
    owner: Agent
    domain_of:
    - Agent
    range: string
class_uri: prov:Agent

```
</details>