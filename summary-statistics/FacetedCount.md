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
| [facet](facet.md) | 0..1 <br/> NONE |  | direct |
| [filtered_count](filtered_count.md) | 1..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) |  | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [edge_count_by_predicate](edge_count_by_predicate.md) | range | [FacetedCount](FacetedCount.md) |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [entailed_edge_count_by_predicate](entailed_edge_count_by_predicate.md) | range | [FacetedCount](FacetedCount.md) |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [synonym_statement_count_by_predicate](synonym_statement_count_by_predicate.md) | range | [FacetedCount](FacetedCount.md) |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [class_count_by_subset](class_count_by_subset.md) | range | [FacetedCount](FacetedCount.md) |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [class_count_by_category](class_count_by_category.md) | range | [FacetedCount](FacetedCount.md) |
| [SummaryStatisticCollection](SummaryStatisticCollection.md) | [mapping_statement_count_by_predicate](mapping_statement_count_by_predicate.md) | range | [FacetedCount](FacetedCount.md) |






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
    rank: 1000
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
    rank: 1000
    key: true
    alias: facet
    owner: FacetedCount
    domain_of:
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