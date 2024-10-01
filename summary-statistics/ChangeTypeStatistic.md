

# Class: ChangeTypeStatistic


_statistics for a particular kind of diff_





URI: [summary_statistics:ChangeTypeStatistic](https://w3id.org/oaklib/summary_statistics.ChangeTypeStatistic)






```{mermaid}
 classDiagram
    class ChangeTypeStatistic
    click ChangeTypeStatistic href "../ChangeTypeStatistic"
      ChangeTypeStatistic : facet
        
      ChangeTypeStatistic : filtered_count
        
      
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
| [UngroupedStatistics](UngroupedStatistics.md) | [change_summary](change_summary.md) | range | [ChangeTypeStatistic](ChangeTypeStatistic.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/summary_statistics




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | summary_statistics:ChangeTypeStatistic |
| native | summary_statistics:ChangeTypeStatistic |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ChangeTypeStatistic
description: statistics for a particular kind of diff
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  facet:
    name: facet
    description: the facet used to group the counts
    from_schema: https://w3id.org/oak/summary_statistics
    key: true
    domain_of:
    - FacetedCount
    - ChangeTypeStatistic
    required: true
  filtered_count:
    name: filtered_count
    description: the number of items in the facet
    from_schema: https://w3id.org/oak/summary_statistics
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
name: ChangeTypeStatistic
description: statistics for a particular kind of diff
from_schema: https://w3id.org/oak/summary_statistics
attributes:
  facet:
    name: facet
    description: the facet used to group the counts
    from_schema: https://w3id.org/oak/summary_statistics
    key: true
    alias: facet
    owner: ChangeTypeStatistic
    domain_of:
    - FacetedCount
    - ChangeTypeStatistic
    range: string
    required: true
  filtered_count:
    name: filtered_count
    description: the number of items in the facet
    from_schema: https://w3id.org/oak/summary_statistics
    alias: filtered_count
    owner: ChangeTypeStatistic
    domain_of:
    - FacetedCount
    - ChangeTypeStatistic
    range: integer
    required: true

```
</details>