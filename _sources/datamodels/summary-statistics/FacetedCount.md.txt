# Class: FacetedCount
_Counts broken down by a facet_




URI: [reporting:FacetedCount](https://w3id.org/linkml/reportFacetedCount)


```{mermaid}
 classDiagram
    class FacetedCount
      FacetedCount : facet
      FacetedCount : filtered_count
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [facet](facet.md) | 0..1 <br/> None | None | direct |
| [filtered_count](filtered_count.md) | 1..1 <br/> integer | None | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [edge_count_by_predicate](edge_count_by_predicate.md) | range | FacetedCount |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [entailed_edge_count_by_predicate](entailed_edge_count_by_predicate.md) | range | FacetedCount |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [synonym_statement_count_by_predicate](synonym_statement_count_by_predicate.md) | range | FacetedCount |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [class_count_by_category](class_count_by_category.md) | range | FacetedCount |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [mapping_statement_count_by_predicate](mapping_statement_count_by_predicate.md) | range | FacetedCount |
| [GlobalStatistics](GlobalStatistics.md) | [edge_count_by_predicate](edge_count_by_predicate.md) | range | FacetedCount |
| [GlobalStatistics](GlobalStatistics.md) | [entailed_edge_count_by_predicate](entailed_edge_count_by_predicate.md) | range | FacetedCount |
| [GlobalStatistics](GlobalStatistics.md) | [synonym_statement_count_by_predicate](synonym_statement_count_by_predicate.md) | range | FacetedCount |
| [GlobalStatistics](GlobalStatistics.md) | [class_count_by_category](class_count_by_category.md) | range | FacetedCount |
| [GlobalStatistics](GlobalStatistics.md) | [mapping_statement_count_by_predicate](mapping_statement_count_by_predicate.md) | range | FacetedCount |
| [FacetStatistics](FacetStatistics.md) | [edge_count_by_predicate](edge_count_by_predicate.md) | range | FacetedCount |
| [FacetStatistics](FacetStatistics.md) | [entailed_edge_count_by_predicate](entailed_edge_count_by_predicate.md) | range | FacetedCount |
| [FacetStatistics](FacetStatistics.md) | [synonym_statement_count_by_predicate](synonym_statement_count_by_predicate.md) | range | FacetedCount |
| [FacetStatistics](FacetStatistics.md) | [class_count_by_category](class_count_by_category.md) | range | FacetedCount |
| [FacetStatistics](FacetStatistics.md) | [mapping_statement_count_by_predicate](mapping_statement_count_by_predicate.md) | range | FacetedCount |







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | reporting:FacetedCount |
| native | reporting:FacetedCount |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: FacetedCount
description: Counts broken down by a facet
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
attributes:
  facet:
    name: facet
    from_schema: https://w3id.org/linkml/summary_statistics
    key: true
  filtered_count:
    name: filtered_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    range: integer
    required: true

```
</details>

### Induced

<details>
```yaml
name: FacetedCount
description: Counts broken down by a facet
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
attributes:
  facet:
    name: facet
    from_schema: https://w3id.org/linkml/summary_statistics
    key: true
    alias: facet
    owner: FacetedCount
    domain_of:
    - FacetStatistics
    - FacetedCount
    range: string
  filtered_count:
    name: filtered_count
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    alias: filtered_count
    owner: FacetedCount
    domain_of:
    - FacetedCount
    range: integer
    required: true

```
</details>