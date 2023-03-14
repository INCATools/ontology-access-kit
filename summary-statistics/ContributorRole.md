# Class: ContributorRole
_A role that a contributor can have_




URI: [sh:ContributorRole](https://w3id.org/shacl/ContributorRole)



```{mermaid}
 classDiagram
    class ContributorRole
      ContributorRole : id
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 0..1 <br/> [String](String.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oaklib/summary_statistics





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
from_schema: https://w3id.org/oaklib/summary_statistics
rank: 1000
attributes:
  id:
    name: id
    description: the unique identifier for the role
    from_schema: https://w3id.org/oaklib/summary_statistics
    identifier: true
    range: uriorcurie
class_uri: sh:ContributorRole

```
</details>

### Induced

<details>
```yaml
name: ContributorRole
description: A role that a contributor can have
from_schema: https://w3id.org/oaklib/summary_statistics
rank: 1000
attributes:
  id:
    name: id
    description: the unique identifier for the role
    from_schema: https://w3id.org/oaklib/summary_statistics
    identifier: true
    alias: id
    owner: ContributorRole
    domain_of:
    - SummaryStatisticsReport
    - Ontology
    - Agent
    - ContributorRole
    range: uriorcurie
class_uri: sh:ContributorRole

```
</details>