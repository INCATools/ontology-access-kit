

# Class: SearchBaseConfiguration


_A user-specified configuration that determines how a particular search operation works_





URI: [ontosearch:SearchBaseConfiguration](https://w3id.org/oak/search-datamodel/SearchBaseConfiguration)






```{mermaid}
 classDiagram
    class SearchBaseConfiguration
    click SearchBaseConfiguration href "../SearchBaseConfiguration"
      SearchBaseConfiguration : categories
        
      SearchBaseConfiguration : cursor
        
      SearchBaseConfiguration : force_case_insensitive
        
      SearchBaseConfiguration : include_obsoletes_in_results
        
      SearchBaseConfiguration : is_complete
        
      SearchBaseConfiguration : is_fuzzy
        
      SearchBaseConfiguration : is_partial
        
      SearchBaseConfiguration : limit
        
      SearchBaseConfiguration : properties
        
          
    
    
    SearchBaseConfiguration --> "*" SearchProperty : properties
    click SearchProperty href "../SearchProperty"

        
      SearchBaseConfiguration : search_terms
        
      SearchBaseConfiguration : syntax
        
          
    
    
    SearchBaseConfiguration --> "0..1" SearchTermSyntax : syntax
    click SearchTermSyntax href "../SearchTermSyntax"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [search_terms](search_terms.md) | * <br/> [SearchTerm](SearchTerm.md) | An individual search term | direct |
| [syntax](syntax.md) | 0..1 <br/> [SearchTermSyntax](SearchTermSyntax.md) | Determines how the search term is interpreted | direct |
| [properties](properties.md) | * <br/> [SearchProperty](SearchProperty.md) | determines which properties are searched over | direct |
| [limit](limit.md) | 0..1 <br/> [Integer](Integer.md) | the maximum number of search results to be returned in one batch | direct |
| [cursor](cursor.md) | 0..1 <br/> [Integer](Integer.md) | when the number of search results exceed the limit this can be used to iterat... | direct |
| [is_partial](is_partial.md) | 0..1 <br/> [Boolean](Boolean.md) | allows matches where the search term is a subset of the full span | direct |
| [is_complete](is_complete.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [include_obsoletes_in_results](include_obsoletes_in_results.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [is_fuzzy](is_fuzzy.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [categories](categories.md) | * <br/> [Uriorcurie](Uriorcurie.md) | categories that should be matched | direct |
| [force_case_insensitive](force_case_insensitive.md) | 0..1 <br/> [Boolean](Boolean.md) | force case insensitive matching | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ComplexQuery](ComplexQuery.md) | [atom](atom.md) | range | [SearchBaseConfiguration](SearchBaseConfiguration.md) |
| [PathExpression](PathExpression.md) | [search_term](search_term.md) | range | [SearchBaseConfiguration](SearchBaseConfiguration.md) |
| [SearchResultSet](SearchResultSet.md) | [configuration](configuration.md) | range | [SearchBaseConfiguration](SearchBaseConfiguration.md) |






## TODOs

* rename this SearchConfiguration

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/search-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontosearch:SearchBaseConfiguration |
| native | ontosearch:SearchBaseConfiguration |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SearchBaseConfiguration
description: A user-specified configuration that determines how a particular search
  operation works
todos:
- rename this SearchConfiguration
from_schema: https://w3id.org/oak/search-datamodel
attributes:
  search_terms:
    name: search_terms
    description: An individual search term. The syntax is determined by the syntax
      slot
    comments:
    - This slot is optional when the configuration is used to parameterize multiple
      searches
    - If multiple terms are provided this is treated as a union query
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: SearchTerm
    multivalued: true
  syntax:
    name: syntax
    description: Determines how the search term is interpreted
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: SearchTermSyntax
  properties:
    name: properties
    description: determines which properties are searched over
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: SearchProperty
    multivalued: true
  limit:
    name: limit
    description: the maximum number of search results to be returned in one batch
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: integer
  cursor:
    name: cursor
    description: when the number of search results exceed the limit this can be used
      to iterate through results
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    - SearchResultSet
    range: integer
  is_partial:
    name: is_partial
    description: allows matches where the search term is a subset of the full span
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  is_complete:
    name: is_complete
    deprecated: use is_partial
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  include_obsoletes_in_results:
    name: include_obsoletes_in_results
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  is_fuzzy:
    name: is_fuzzy
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  categories:
    name: categories
    description: categories that should be matched
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: uriorcurie
    multivalued: true
  force_case_insensitive:
    name: force_case_insensitive
    description: force case insensitive matching
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchBaseConfiguration
    range: boolean

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
from_schema: https://w3id.org/oak/search-datamodel
attributes:
  search_terms:
    name: search_terms
    description: An individual search term. The syntax is determined by the syntax
      slot
    comments:
    - This slot is optional when the configuration is used to parameterize multiple
      searches
    - If multiple terms are provided this is treated as a union query
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: search_terms
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: SearchTerm
    multivalued: true
  syntax:
    name: syntax
    description: Determines how the search term is interpreted
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: syntax
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: SearchTermSyntax
  properties:
    name: properties
    description: determines which properties are searched over
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: properties
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: SearchProperty
    multivalued: true
  limit:
    name: limit
    description: the maximum number of search results to be returned in one batch
    from_schema: https://w3id.org/oak/search-datamodel
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
    from_schema: https://w3id.org/oak/search-datamodel
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
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: is_partial
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  is_complete:
    name: is_complete
    deprecated: use is_partial
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: is_complete
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  include_obsoletes_in_results:
    name: include_obsoletes_in_results
    deprecated: use properties to explicitly list properties
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: include_obsoletes_in_results
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  is_fuzzy:
    name: is_fuzzy
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: is_fuzzy
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: boolean
  categories:
    name: categories
    description: categories that should be matched
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: categories
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: uriorcurie
    multivalued: true
  force_case_insensitive:
    name: force_case_insensitive
    description: force case insensitive matching
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: force_case_insensitive
    owner: SearchBaseConfiguration
    domain_of:
    - SearchBaseConfiguration
    range: boolean

```
</details>