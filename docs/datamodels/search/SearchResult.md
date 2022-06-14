# Class: SearchResult
_An individual search result_





URI: [search:SearchResult](https://w3id.org/linkml/search_datamodel/SearchResult)




```{mermaid}
 classDiagram
    class SearchResult
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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [rank](rank.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | For relevancy-ranked results, this indicates the relevancy, with low numbers being the most relevant  | . |
| [object_id](object_id.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 1..1 | The CURIE of the matched term  | . |
| [object_label](object_label.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 _recommended_ | The label/name of the matched term  | . |
| [object_source](object_source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | The ontology or other source that contains the matched term  | . |
| [object_source_version](object_source_version.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | Version IRI or version string of the source of the object term.  | . |
| [object_match_field](object_match_field.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | The field/property in which the match was found  | . |
| [matches_full_search_term](matches_full_search_term.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | Does the matched field match the full string  | . |
| [snippet](snippet.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | shows how the field was matched  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [SearchResultSet](SearchResultSet.md) | [results](results.md) | range | SearchResult |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/search_datamodel







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['search:SearchResult'] |
| native | ['search:SearchResult'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SearchResult
description: An individual search result
from_schema: https://w3id.org/linkml/search_datamodel
attributes:
  rank:
    name: rank
    description: For relevancy-ranked results, this indicates the relevancy, with
      low numbers being the most relevant
    from_schema: https://w3id.org/linkml/search_datamodel
    range: integer
  object_id:
    name: object_id
    description: The CURIE of the matched term
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_id
    required: true
  object_label:
    name: object_label
    description: The label/name of the matched term
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_label
    recommended: true
  object_source:
    name: object_source
    description: The ontology or other source that contains the matched term
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_source
  object_source_version:
    name: object_source_version
    description: Version IRI or version string of the source of the object term.
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_source_version
  object_match_field:
    name: object_match_field
    description: The field/property in which the match was found
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_match_field
  matches_full_search_term:
    name: matches_full_search_term
    description: Does the matched field match the full string
    from_schema: https://w3id.org/linkml/search_datamodel
    range: boolean
  snippet:
    name: snippet
    description: shows how the field was matched
    from_schema: https://w3id.org/linkml/search_datamodel

```
</details>

### Induced

<details>
```yaml
name: SearchResult
description: An individual search result
from_schema: https://w3id.org/linkml/search_datamodel
attributes:
  rank:
    name: rank
    description: For relevancy-ranked results, this indicates the relevancy, with
      low numbers being the most relevant
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: rank
    owner: SearchResult
    range: integer
  object_id:
    name: object_id
    description: The CURIE of the matched term
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_id
    alias: object_id
    owner: SearchResult
    range: string
    required: true
  object_label:
    name: object_label
    description: The label/name of the matched term
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_label
    alias: object_label
    owner: SearchResult
    range: string
    recommended: true
  object_source:
    name: object_source
    description: The ontology or other source that contains the matched term
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_source
    alias: object_source
    owner: SearchResult
    range: string
  object_source_version:
    name: object_source_version
    description: Version IRI or version string of the source of the object term.
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_source_version
    alias: object_source_version
    owner: SearchResult
    range: string
  object_match_field:
    name: object_match_field
    description: The field/property in which the match was found
    from_schema: https://w3id.org/linkml/search_datamodel
    slot_uri: sssom:object_match_field
    alias: object_match_field
    owner: SearchResult
    range: string
  matches_full_search_term:
    name: matches_full_search_term
    description: Does the matched field match the full string
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: matches_full_search_term
    owner: SearchResult
    range: boolean
  snippet:
    name: snippet
    description: shows how the field was matched
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: snippet
    owner: SearchResult
    range: string

```
</details>