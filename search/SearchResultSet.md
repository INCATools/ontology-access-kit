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

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [configuration](configuration.md) | 0..1 <br/> [SearchBaseConfiguration](SearchBaseConfiguration.md)  |   |
| [results](results.md) | 0..* <br/> [SearchResult](SearchResult.md)  |   |
| [result_count](result_count.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |
| [cursor](cursor.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  |   |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/search_datamodel







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['search:SearchResultSet'] |
| native | ['search:SearchResultSet'] |


## LinkML Specification

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