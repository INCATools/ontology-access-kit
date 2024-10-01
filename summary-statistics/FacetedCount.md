

# Class: FacetedCount


_Counts broken down by a facet_





URI: [summary_statistics:FacetedCount](https://w3id.org/oaklib/summary_statistics.FacetedCount)






```{mermaid}
 classDiagram
    class FacetedCount
    click FacetedCount href "../FacetedCount"
      FacetedCount : facet
        
      FacetedCount : filtered_count
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [facet](facet.md) | 0..1 <br/> [String](String.md) | the facet used to group the counts | direct |
| [filtered_count](filtered_count.md) | 1 <br/> [Integer](Integer.md) | the number of items in the facet | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [UngroupedStatistics](UngroupedStatistics.md) | [edge_count_by_predicate](edge_count_by_predicate.md) | range | [FacetedCount](FacetedCount.md) |
| [UngroupedStatistics](UngroupedStatistics.md) | [entailed_edge_count_by_predicate](entailed_edge_count_by_predicate.md) | range | [FacetedCount](FacetedCount.md) |
| [UngroupedStatistics](UngroupedStatistics.md) | [synonym_statement_count_by_predicate](synonym_statement_count_by_predicate.md) | range | [FacetedCount](FacetedCount.md) |
| [UngroupedStatistics](UngroupedStatistics.md) | [class_count_by_subset](class_count_by_subset.md) | range | [FacetedCount](FacetedCount.md) |
| [UngroupedStatistics](UngroupedStatistics.md) | [class_count_by_category](class_count_by_category.md) | range | [FacetedCount](FacetedCount.md) |
| [UngroupedStatistics](UngroupedStatistics.md) | [mapping_statement_count_by_predicate](mapping_statement_count_by_predicate.md) | range | [FacetedCount](FacetedCount.md) |
| [UngroupedStatistics](UngroupedStatistics.md) | [mapping_statement_count_by_object_source](mapping_statement_count_by_object_source.md) | range | [FacetedCount](FacetedCount.md) |
| [UngroupedStatistics](UngroupedStatistics.md) | [mapping_statement_count_subject_by_object_source](mapping_statement_count_subject_by_object_source.md) | range | [FacetedCount](FacetedCount.md) |
| [ContributorStatistics](ContributorStatistics.md) | [role_counts](role_counts.md) | range | [FacetedCount](FacetedCount.md) |






## Comments

* For example, edge counts may be grouped by predicate (relationship type)

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:FacetedCount |
| native | summary_statistics:FacetedCount |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: FacetedCount
description: Counts broken down by a facet
comments:
- For example, edge counts may be grouped by predicate (relationship type)
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  facet:
    name: facet
    description: the facet used to group the counts
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    key: true
    domain_of:
    - FacetedCount
    - ChangeTypeStatistic
    required: true
  filtered_count:
    name: filtered_count
    description: the number of items in the facet
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    domain_of:
    - FacetedCount
    - ChangeTypeStatistic
    range: integer
    required: true

```
</details>

### Induced

<details>
```yaml
name: FacetedCount
description: Counts broken down by a facet
comments:
- For example, edge counts may be grouped by predicate (relationship type)
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  facet:
    name: facet
    description: the facet used to group the counts
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    key: true
    alias: facet
    owner: FacetedCount
    domain_of:
    - FacetedCount
    - ChangeTypeStatistic
    range: string
    required: true
  filtered_count:
    name: filtered_count
    description: the number of items in the facet
    from_schema: https://w3id.org/oak/summary_statistics
    rank: 1000
    alias: filtered_count
    owner: FacetedCount
    domain_of:
    - FacetedCount
    - ChangeTypeStatistic
    range: integer
    required: true

```
</details>