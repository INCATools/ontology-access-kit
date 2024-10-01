

# Class: SearchResult


_An individual search result_





URI: [ontosearch:SearchResult](https://w3id.org/oak/search-datamodel/SearchResult)






```{mermaid}
 classDiagram
    class SearchResult
    click SearchResult href "../SearchResult"
      SearchResult : matches_full_search_term
        
      SearchResult : object_id
        
      SearchResult : object_label
        
      SearchResult : object_match_field
        
      SearchResult : object_source
        
      SearchResult : object_source_version
        
      SearchResult : rank
        
      SearchResult : snippet
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [rank](rank.md) | 0..1 <br/> [Integer](Integer.md) | For relevancy-ranked results, this indicates the relevancy, with low numbers ... | direct |
| [object_id](object_id.md) | 1 <br/> [String](String.md) | The CURIE of the matched term | direct |
| [object_label](object_label.md) | 0..1 _recommended_ <br/> [String](String.md) | The label/name of the matched term | direct |
| [object_source](object_source.md) | 0..1 <br/> [String](String.md) | The ontology or other source that contains the matched term | direct |
| [object_source_version](object_source_version.md) | 0..1 <br/> [String](String.md) | Version IRI or version string of the source of the object term | direct |
| [object_match_field](object_match_field.md) | 0..1 <br/> [String](String.md) | The field/property in which the match was found | direct |
| [matches_full_search_term](matches_full_search_term.md) | 0..1 <br/> [Boolean](Boolean.md) | Does the matched field match the full string | direct |
| [snippet](snippet.md) | 0..1 <br/> [String](String.md) | shows how the field was matched | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SearchResultSet](SearchResultSet.md) | [results](results.md) | range | [SearchResult](SearchResult.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/search-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontosearch:SearchResult |
| native | ontosearch:SearchResult |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SearchResult
description: An individual search result
from_schema: https://w3id.org/oak/search-datamodel
attributes:
  rank:
    name: rank
    description: For relevancy-ranked results, this indicates the relevancy, with
      low numbers being the most relevant
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchResult
    range: integer
  object_id:
    name: object_id
    description: The CURIE of the matched term
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_id
    domain_of:
    - SearchResult
    required: true
  object_label:
    name: object_label
    description: The label/name of the matched term
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_label
    domain_of:
    - SearchResult
    recommended: true
  object_source:
    name: object_source
    description: The ontology or other source that contains the matched term
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_source
    domain_of:
    - SearchResult
  object_source_version:
    name: object_source_version
    description: Version IRI or version string of the source of the object term.
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_source_version
    domain_of:
    - SearchResult
  object_match_field:
    name: object_match_field
    description: The field/property in which the match was found
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_match_field
    domain_of:
    - SearchResult
  matches_full_search_term:
    name: matches_full_search_term
    description: Does the matched field match the full string
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchResult
    range: boolean
  snippet:
    name: snippet
    description: shows how the field was matched
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - SearchResult

```
</details>

### Induced

<details>
```yaml
name: SearchResult
description: An individual search result
from_schema: https://w3id.org/oak/search-datamodel
attributes:
  rank:
    name: rank
    description: For relevancy-ranked results, this indicates the relevancy, with
      low numbers being the most relevant
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: rank
    owner: SearchResult
    domain_of:
    - SearchResult
    range: integer
  object_id:
    name: object_id
    description: The CURIE of the matched term
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_id
    alias: object_id
    owner: SearchResult
    domain_of:
    - SearchResult
    range: string
    required: true
  object_label:
    name: object_label
    description: The label/name of the matched term
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_label
    alias: object_label
    owner: SearchResult
    domain_of:
    - SearchResult
    range: string
    recommended: true
  object_source:
    name: object_source
    description: The ontology or other source that contains the matched term
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_source
    alias: object_source
    owner: SearchResult
    domain_of:
    - SearchResult
    range: string
  object_source_version:
    name: object_source_version
    description: Version IRI or version string of the source of the object term.
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_source_version
    alias: object_source_version
    owner: SearchResult
    domain_of:
    - SearchResult
    range: string
  object_match_field:
    name: object_match_field
    description: The field/property in which the match was found
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    slot_uri: sssom:object_match_field
    alias: object_match_field
    owner: SearchResult
    domain_of:
    - SearchResult
    range: string
  matches_full_search_term:
    name: matches_full_search_term
    description: Does the matched field match the full string
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: matches_full_search_term
    owner: SearchResult
    domain_of:
    - SearchResult
    range: boolean
  snippet:
    name: snippet
    description: shows how the field was matched
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: snippet
    owner: SearchResult
    domain_of:
    - SearchResult
    range: string

```
</details>