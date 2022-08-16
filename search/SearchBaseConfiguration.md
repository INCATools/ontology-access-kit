# Class: SearchBaseConfiguration
_A user-specified configuration that determines how a particular search operation works_





URI: [search:SearchBaseConfiguration](https://w3id.org/linkml/search_datamodel/SearchBaseConfiguration)




```{mermaid}
 classDiagram
    class SearchBaseConfiguration
      SearchBaseConfiguration : categories
      SearchBaseConfiguration : cursor
      SearchBaseConfiguration : include_obsoletes_in_results
      SearchBaseConfiguration : is_complete
      SearchBaseConfiguration : is_fuzzy
      SearchBaseConfiguration : is_partial
      SearchBaseConfiguration : limit
      SearchBaseConfiguration : properties
      SearchBaseConfiguration : search_terms
      SearchBaseConfiguration : syntax
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [search_terms](search_terms.md) | 0..* <br/> [SearchTerm](SearchTerm.md)  | An individual search term  |
| [syntax](syntax.md) | 0..1 <br/> [SearchTermSyntax](SearchTermSyntax.md)  | Determines how the search term is interpreted  |
| [properties](properties.md) | 0..* <br/> [SearchProperty](SearchProperty.md)  | determines which properties are searched over  |
| [limit](limit.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  | the maximum number of search results to be returned in one batch  |
| [cursor](cursor.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer)  | when the number of search results exceed the limit this can be used to iterat...  |
| [is_partial](is_partial.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean)  | allows matches where the search term is a subset of the full span  |
| [is_complete](is_complete.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean)  |   |
| [include_obsoletes_in_results](include_obsoletes_in_results.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean)  |   |
| [is_fuzzy](is_fuzzy.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean)  |   |
| [categories](categories.md) | 0..* <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)  | categories that should be matched  |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ComplexQuery](ComplexQuery.md) | [atom](atom.md) | range | SearchBaseConfiguration |
| [PathExpression](PathExpression.md) | [search_term](search_term.md) | range | SearchBaseConfiguration |
| [SearchResultSet](SearchResultSet.md) | [configuration](configuration.md) | range | SearchBaseConfiguration |



## TODOs

* rename this SearchConfiguration

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/search_datamodel







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['search:SearchBaseConfiguration'] |
| native | ['search:SearchBaseConfiguration'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SearchBaseConfiguration
description: A user-specified configuration that determines how a particular search
  operation works
todos:
- rename this SearchConfiguration
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
attributes:
  search_terms:
    name: search_terms
    description: An individual search term. The syntax is determined by the syntax
      slot
    comments:
    - This slot is optional when the configuration is used to paramterize multiple
      searches
    - If multiple terms are provided this is treated as a union query
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    range: SearchTerm
  syntax:
    name: syntax
    description: Determines how the search term is interpreted
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: SearchTermSyntax
  properties:
    name: properties
    description: determines which properties are searched over
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    range: SearchProperty
  limit:
    name: limit
    description: the maximum number of search results to be returned in one batch
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: integer
  cursor:
    name: cursor
    description: when the number of search results exceed the limit this can be used
      to iterate through results
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: integer
  is_partial:
    name: is_partial
    description: allows matches where the search term is a subset of the full span
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: boolean
  is_complete:
    name: is_complete
    deprecated: use is_partial
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: boolean
  include_obsoletes_in_results:
    name: include_obsoletes_in_results
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: boolean
  is_fuzzy:
    name: is_fuzzy
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: boolean
  categories:
    name: categories
    description: categories that should be matched
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    range: uriorcurie

```
</details>

### Induced

<details>
```yaml
name: SearchBaseConfiguration
description: A user-specified configuration that determines how a particular search
  operation works
todos:
- rename this SearchConfiguration
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
attributes:
  search_terms:
    name: search_terms
    description: An individual search term. The syntax is determined by the syntax
      slot
    comments:
    - This slot is optional when the configuration is used to paramterize multiple
      searches
    - If multiple terms are provided this is treated as a union query
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    alias: search_terms
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: SearchTerm
  syntax:
    name: syntax
    description: Determines how the search term is interpreted
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: syntax
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: SearchTermSyntax
  properties:
    name: properties
    description: determines which properties are searched over
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    alias: properties
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: SearchProperty
  limit:
    name: limit
    description: the maximum number of search results to be returned in one batch
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: limit
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: integer
  cursor:
    name: cursor
    description: when the number of search results exceed the limit this can be used
      to iterate through results
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: cursor
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    - SearchResultSet
    range: integer
  is_partial:
    name: is_partial
    description: allows matches where the search term is a subset of the full span
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: is_partial
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  is_complete:
    name: is_complete
    deprecated: use is_partial
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: is_complete
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  include_obsoletes_in_results:
    name: include_obsoletes_in_results
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: include_obsoletes_in_results
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  is_fuzzy:
    name: is_fuzzy
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: is_fuzzy
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  categories:
    name: categories
    description: categories that should be matched
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    alias: categories
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: uriorcurie

```
</details>