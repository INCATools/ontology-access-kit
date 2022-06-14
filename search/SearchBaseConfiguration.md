# Class: SearchBaseConfiguration
_A user-specified configuration that determines how a particular search operation works_





URI: [search:SearchBaseConfiguration](https://w3id.org/linkml/search_datamodel/SearchBaseConfiguration)




```{mermaid}
 classDiagram
    class SearchBaseConfiguration
      SearchBaseConfiguration : categories
      SearchBaseConfiguration : cursor
      SearchBaseConfiguration : include_aliases
      SearchBaseConfiguration : include_definition
      SearchBaseConfiguration : include_id
      SearchBaseConfiguration : include_label
      SearchBaseConfiguration : include_obsoletes_in_results
      SearchBaseConfiguration : is_complete
      SearchBaseConfiguration : is_partial
      SearchBaseConfiguration : is_regular_expression
      SearchBaseConfiguration : limit
      SearchBaseConfiguration : properties
      SearchBaseConfiguration : search_terms
      SearchBaseConfiguration : syntax
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [search_terms](search_terms.md) | [SearchTerm](SearchTerm.md) | 0..* | An individual search term. The syntax is determined by the syntax slot  | . |
| [syntax](syntax.md) | [SearchTermSyntax](SearchTermSyntax.md) | 0..1 | Determines how the search term is interpreted  | . |
| [properties](properties.md) | [SearchProperty](SearchProperty.md) | 0..* | determines which properties are searched over  | . |
| [limit](limit.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | the maximum number of search results to be returned in one batch  | . |
| [cursor](cursor.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | when the number of search results exceed the limit this can be used to iterate through results  | . |
| [is_regular_expression](is_regular_expression.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [is_partial](is_partial.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [is_complete](is_complete.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | restricts search results to matches of the full span of the string  | . |
| [include_id](include_id.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [include_label](include_label.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [include_aliases](include_aliases.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [include_definition](include_definition.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [include_obsoletes_in_results](include_obsoletes_in_results.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [categories](categories.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [AtomicQuery](AtomicQuery.md) | [search_term](search_term.md) | range | SearchBaseConfiguration |
| [SearchResultSet](SearchResultSet.md) | [configuration](configuration.md) | range | SearchBaseConfiguration |



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
from_schema: https://w3id.org/linkml/search_datamodel
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
    multivalued: true
    range: SearchTerm
  syntax:
    name: syntax
    description: Determines how the search term is interpreted
    from_schema: https://w3id.org/linkml/search_datamodel
    range: SearchTermSyntax
  properties:
    name: properties
    description: determines which properties are searched over
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true
    range: SearchProperty
  limit:
    name: limit
    description: the maximum number of search results to be returned in one batch
    from_schema: https://w3id.org/linkml/search_datamodel
    range: integer
  cursor:
    name: cursor
    description: when the number of search results exceed the limit this can be used
      to iterate through results
    from_schema: https://w3id.org/linkml/search_datamodel
    range: integer
  is_regular_expression:
    name: is_regular_expression
    deprecated: use the syntax slot
    from_schema: https://w3id.org/linkml/search_datamodel
    range: boolean
  is_partial:
    name: is_partial
    deprecated: use is_complete
    from_schema: https://w3id.org/linkml/search_datamodel
    range: boolean
  is_complete:
    name: is_complete
    description: restricts search results to matches of the full span of the string
    from_schema: https://w3id.org/linkml/search_datamodel
    range: boolean
  include_id:
    name: include_id
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    range: boolean
  include_label:
    name: include_label
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    range: boolean
  include_aliases:
    name: include_aliases
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    range: boolean
  include_definition:
    name: include_definition
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    range: boolean
  include_obsoletes_in_results:
    name: include_obsoletes_in_results
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    range: boolean
  categories:
    name: categories
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: SearchBaseConfiguration
description: A user-specified configuration that determines how a particular search
  operation works
from_schema: https://w3id.org/linkml/search_datamodel
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
    multivalued: true
    alias: search_terms
    owner: SearchBaseConfiguration
    range: SearchTerm
  syntax:
    name: syntax
    description: Determines how the search term is interpreted
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: syntax
    owner: SearchBaseConfiguration
    range: SearchTermSyntax
  properties:
    name: properties
    description: determines which properties are searched over
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true
    alias: properties
    owner: SearchBaseConfiguration
    range: SearchProperty
  limit:
    name: limit
    description: the maximum number of search results to be returned in one batch
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: limit
    owner: SearchBaseConfiguration
    range: integer
  cursor:
    name: cursor
    description: when the number of search results exceed the limit this can be used
      to iterate through results
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: cursor
    owner: SearchBaseConfiguration
    range: integer
  is_regular_expression:
    name: is_regular_expression
    deprecated: use the syntax slot
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: is_regular_expression
    owner: SearchBaseConfiguration
    range: boolean
  is_partial:
    name: is_partial
    deprecated: use is_complete
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: is_partial
    owner: SearchBaseConfiguration
    range: boolean
  is_complete:
    name: is_complete
    description: restricts search results to matches of the full span of the string
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: is_complete
    owner: SearchBaseConfiguration
    range: boolean
  include_id:
    name: include_id
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: include_id
    owner: SearchBaseConfiguration
    range: boolean
  include_label:
    name: include_label
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: include_label
    owner: SearchBaseConfiguration
    range: boolean
  include_aliases:
    name: include_aliases
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: include_aliases
    owner: SearchBaseConfiguration
    range: boolean
  include_definition:
    name: include_definition
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: include_definition
    owner: SearchBaseConfiguration
    range: boolean
  include_obsoletes_in_results:
    name: include_obsoletes_in_results
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: include_obsoletes_in_results
    owner: SearchBaseConfiguration
    range: boolean
  categories:
    name: categories
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true
    alias: categories
    owner: SearchBaseConfiguration
    range: string

```
</details>