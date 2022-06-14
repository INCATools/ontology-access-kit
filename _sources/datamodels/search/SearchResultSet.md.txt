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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [configuration](configuration.md) | [SearchBaseConfiguration](SearchBaseConfiguration.md) | 0..1 | None  | . |
| [results](results.md) | [SearchResult](SearchResult.md) | 0..* | None  | . |
| [result_count](result_count.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [cursor](cursor.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |


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
attributes:
  configuration:
    name: configuration
    from_schema: https://w3id.org/linkml/search_datamodel
    range: SearchBaseConfiguration
  results:
    name: results
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true
    range: SearchResult
  result_count:
    name: result_count
    from_schema: https://w3id.org/linkml/search_datamodel
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
attributes:
  configuration:
    name: configuration
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: configuration
    owner: SearchResultSet
    range: SearchBaseConfiguration
  results:
    name: results
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true
    alias: results
    owner: SearchResultSet
    range: SearchResult
  result_count:
    name: result_count
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: result_count
    owner: SearchResultSet
    range: integer
  cursor:
    name: cursor
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: cursor
    owner: SearchResultSet
    range: integer

```
</details>