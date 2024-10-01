

# Class: ContributorRole


_A role that a contributor can have_





URI: [sh:ContributorRole](https://w3id.org/shacl/ContributorRole)






```{mermaid}
 classDiagram
    class ContributorRole
    click ContributorRole href "../ContributorRole"
      ContributorRole : id
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | the unique identifier for the role | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:ContributorRole |
| native | summary_statistics:ContributorRole |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ContributorRole
description: A role that a contributor can have
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  id:
    name: id
    description: the unique identifier for the role
    from_schema: https://w3id.org/oak/summary_statistics
    identifier: true
    domain_of:
    - SummaryStatisticsReport
    - Ontology
    - Agent
    - ContributorRole
    range: uriorcurie
    required: true
class_uri: sh:ContributorRole

```
</details>

### Induced

<details>
```yaml
name: ContributorRole
description: A role that a contributor can have
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  id:
    name: id
    description: the unique identifier for the role
    from_schema: https://w3id.org/oak/summary_statistics
    identifier: true
    alias: id
    owner: ContributorRole
    domain_of:
    - SummaryStatisticsReport
    - Ontology
    - Agent
    - ContributorRole
    range: uriorcurie
    required: true
class_uri: sh:ContributorRole

```
</details>