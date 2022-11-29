# Class: GlobalStatistics
_summary statistics for the entire resource_




URI: [reporting:GlobalStatistics](https://w3id.org/linkml/reportGlobalStatistics)


```{mermaid}
 classDiagram
    class GlobalStatistics
      GlobalStatistics : description
      GlobalStatistics : partitions
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [description](description.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [partitions](partitions.md) | 0..* <br/> [SummaryStatisticCollection](SummaryStatisticCollection.md) | statistics keyed by category | direct |







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/summary_statistics





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | reporting:GlobalStatistics |
| native | reporting:GlobalStatistics |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: GlobalStatistics
description: summary statistics for the entire resource
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
attributes:
  description:
    name: description
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    range: string
  partitions:
    name: partitions
    description: statistics keyed by category
    comments:
    - for example, GO stats may be broken out by MF/BP/CC
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    range: SummaryStatisticCollection
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: GlobalStatistics
description: summary statistics for the entire resource
from_schema: https://w3id.org/linkml/summary_statistics
rank: 1000
attributes:
  description:
    name: description
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    alias: description
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: string
  partitions:
    name: partitions
    description: statistics keyed by category
    comments:
    - for example, GO stats may be broken out by MF/BP/CC
    from_schema: https://w3id.org/linkml/summary_statistics
    rank: 1000
    multivalued: true
    alias: partitions
    owner: GlobalStatistics
    domain_of:
    - GlobalStatistics
    range: SummaryStatisticCollection
    inlined: true

```
</details>