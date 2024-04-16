

# Class: SearchResultSet



URI: [ontosearch:SearchResultSet](https://w3id.org/oak/search-datamodel/SearchResultSet)




```{mermaid}
 classDiagram
    class SearchResultSet
      SearchResultSet : configuration
        
          SearchResultSet --> SearchBaseConfiguration : configuration
        
      SearchResultSet : cursor
        
      SearchResultSet : result_count
        
      SearchResultSet : results
        
          SearchResultSet --> SearchResult : results
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [configuration](configuration.md) | 0..1 <br/> [SearchBaseConfiguration](SearchBaseConfiguration.md) |  | direct |
| [results](results.md) | 0..* <br/> [SearchResult](SearchResult.md) |  | direct |
| [result_count](result_count.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |
| [cursor](cursor.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/search-datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontosearch:SearchResultSet |
| native | ontosearch:SearchResultSet |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SearchResultSet
from_schema: https://w3id.org/oak/search-datamodel
attributes:
  configuration:
    name: configuration
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchResultSet
    range: SearchBaseConfiguration
  results:
    name: results
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    multivalued: true
    domain_of:
    - SearchResultSet
    range: SearchResult
  result_count:
    name: result_count
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchResultSet
    range: integer
  cursor:
    name: cursor
    from_schema: https://w3id.org/oak/search-datamodel
    domain_of:
    - SearchBaseConfiguration
    - SearchResultSet
    range: integer

```
</details>

### Induced

<details>
```yaml
name: SearchResultSet
from_schema: https://w3id.org/oak/search-datamodel
attributes:
  configuration:
    name: configuration
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: configuration
    owner: SearchResultSet
    domain_of:
    - SearchResultSet
    range: SearchBaseConfiguration
  results:
    name: results
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    multivalued: true
    alias: results
    owner: SearchResultSet
    domain_of:
    - SearchResultSet
    range: SearchResult
  result_count:
    name: result_count
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: result_count
    owner: SearchResultSet
    domain_of:
    - SearchResultSet
    range: integer
  cursor:
    name: cursor
    from_schema: https://w3id.org/oak/search-datamodel
    alias: cursor
    owner: SearchResultSet
    domain_of:
    - SearchBaseConfiguration
    - SearchResultSet
    range: integer

```
</details>