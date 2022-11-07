# Class: SearchResultSet



URI: [search:SearchResultSet](https://w3id.org/linkml/search_datamodel/SearchResultSet)


```{mermaid}
 classDiagram
    class SearchResultSet
      SearchResultSet : configuration
      SearchResultSet : cursor
      SearchResultSet : result_count
      SearchResultSet : results
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [configuration](configuration.md) | 0..1 <br/> SearchBaseConfiguration | None | direct |
| [results](results.md) | 0..* <br/> SearchResult | None | direct |
| [result_count](result_count.md) | 0..1 <br/> integer | None | direct |
| [cursor](cursor.md) | 0..1 <br/> None | None | direct |








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/search_datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | search:SearchResultSet |
| native | search:SearchResultSet |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SearchResultSet
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
attributes:
  configuration:
    name: configuration
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: SearchBaseConfiguration
  results:
    name: results
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    range: SearchResult
  result_count:
    name: result_count
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: integer
  cursor:
    name: cursor
    from_schema: https://w3id.org/linkml/search_datamodel
    range: integer

```
</details>

### Induced

<details>
```yaml
name: SearchResultSet
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
attributes:
  configuration:
    name: configuration
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: configuration
    owner: SearchResultSet
    domain_of:
    - SearchResultSet
    range: SearchBaseConfiguration
  results:
    name: results
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    alias: results
    owner: SearchResultSet
    domain_of:
    - SearchResultSet
    range: SearchResult
  result_count:
    name: result_count
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: result_count
    owner: SearchResultSet
    domain_of:
    - SearchResultSet
    range: integer
  cursor:
    name: cursor
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: cursor
    owner: SearchResultSet
    domain_of:
    - SearchBaseConfiguration
    - SearchResultSet
    range: integer

```
</details>