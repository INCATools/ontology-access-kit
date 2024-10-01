

# Class: ContributorStatistics


_Statistics for a contributor_





URI: [summary_statistics:ContributorStatistics](https://w3id.org/oaklib/summary_statistics.ContributorStatistics)






```{mermaid}
 classDiagram
    class ContributorStatistics
    click ContributorStatistics href "../ContributorStatistics"
      ContributorStatistics : contributor_id
        
      ContributorStatistics : contributor_name
        
      ContributorStatistics : normalization_comments
        
      ContributorStatistics : role_counts
        
          
    
    
    ContributorStatistics --> "*" FacetedCount : role_counts
    click FacetedCount href "../FacetedCount"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [contributor_id](contributor_id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | the contributor | direct |
| [contributor_name](contributor_name.md) | 0..1 <br/> [String](String.md) | the name of the contributor | direct |
| [normalization_comments](normalization_comments.md) | 0..1 <br/> [String](String.md) | if contributor name normalization was applied, provide details here | direct |
| [role_counts](role_counts.md) | * <br/> [FacetedCount](FacetedCount.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [UngroupedStatistics](UngroupedStatistics.md) | [contributor_summary](contributor_summary.md) | range | [ContributorStatistics](ContributorStatistics.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:ContributorStatistics |
| native | summary_statistics:ContributorStatistics |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ContributorStatistics
description: Statistics for a contributor
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  contributor_id:
    name: contributor_id
    description: the contributor
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    key: true
    domain_of:
    - ContributorStatistics
    range: uriorcurie
    required: true
  contributor_name:
    name: contributor_name
    description: the name of the contributor
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - ContributorStatistics
    range: string
  normalization_comments:
    name: normalization_comments
    description: if contributor name normalization was applied, provide details here
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - ContributorStatistics
    range: string
  role_counts:
    name: role_counts
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - ContributorStatistics
    range: FacetedCount
    multivalued: true
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: ContributorStatistics
description: Statistics for a contributor
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  contributor_id:
    name: contributor_id
    description: the contributor
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    key: true
    alias: contributor_id
    owner: ContributorStatistics
    domain_of:
    - ContributorStatistics
    range: uriorcurie
    required: true
  contributor_name:
    name: contributor_name
    description: the name of the contributor
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: contributor_name
    owner: ContributorStatistics
    domain_of:
    - ContributorStatistics
    range: string
  normalization_comments:
    name: normalization_comments
    description: if contributor name normalization was applied, provide details here
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: normalization_comments
    owner: ContributorStatistics
    domain_of:
    - ContributorStatistics
    range: string
  role_counts:
    name: role_counts
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: role_counts
    owner: ContributorStatistics
    domain_of:
    - ContributorStatistics
    range: FacetedCount
    multivalued: true
    inlined: true

```
</details>