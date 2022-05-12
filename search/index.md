# search-datamodel

A datamodel for representing a search configuration and results. This is intended to provide a unified layer over both (a) how searches are *parameterized* (b) the structure of search *results*. The scope is any kind of service that provides search over *named entities*, including ontology concepts. It is not intended to cover generic search results, e.g. google search, although parts could be generalized for this purpose.

URI: https://w3id.org/linkml/search_datamodel

## Classes

| Class | Description |
| --- | --- |
| [SearchBaseConfiguration](SearchBaseConfiguration.md) | A user-specified configuration that determines how a particular search operation works | 
| [BooleanQuery](BooleanQuery.md) | None | 
| [AtomicQuery](AtomicQuery.md) | None | 
| [SearchResult](SearchResult.md) | An individual search result | 
| [SearchResultSet](SearchResultSet.md) | None | 


## Slots

| Slot | Description |
| --- | --- |
| [search_terms](search_terms.md) | An individual search term. The syntax is determined by the syntax slot | 
| [syntax](syntax.md) | Determines how the search term is interpreted | 
| [properties](properties.md) | determines which properties are searched over | 
| [limit](limit.md) | the maximum number of search results to be returned in one batch | 
| [cursor](cursor.md) | when the number of search results exceed the limit this can be used to iterate through results | 
| [is_regular_expression](is_regular_expression.md) | None | 
| [is_partial](is_partial.md) | None | 
| [is_complete](is_complete.md) | restricts search results to matches of the full span of the string | 
| [include_id](include_id.md) | None | 
| [include_label](include_label.md) | None | 
| [include_aliases](include_aliases.md) | None | 
| [include_definition](include_definition.md) | None | 
| [include_obsoletes_in_results](include_obsoletes_in_results.md) | None | 
| [categories](categories.md) | None | 
| [operator](operator.md) | None | 
| [operands](operands.md) | None | 
| [atom](atom.md) | None | 
| [graph_function](graph_function.md) | None | 
| [graph_predicates](graph_predicates.md) | None | 
| [search_term](search_term.md) | None | 
| [rank](rank.md) | For relevancy-ranked results, this indicates the relevancy, with low numbers being the most relevant | 
| [object_id](object_id.md) | The CURIE of the matched term | 
| [object_label](object_label.md) | The label/name of the matched term | 
| [object_source](object_source.md) | The ontology or other source that contains the matched term | 
| [object_source_version](object_source_version.md) | Version IRI or version string of the source of the object term. | 
| [object_match_field](object_match_field.md) | The field/property in which the match was found | 
| [matches_full_search_term](matches_full_search_term.md) | Does the matched field match the full string | 
| [snippet](snippet.md) | shows how the field was matched | 
| [configuration](configuration.md) | None | 
| [results](results.md) | None | 
| [result_count](result_count.md) | None | 


## Enums

| Enums | Description |
| --- | --- |
| [SearchTermSyntax](SearchTermSyntax.md) | None | 
| [SearchProperty](SearchProperty.md) | A property that can be searched on | 
| [BooleanOperator](BooleanOperator.md) | None | 
| [GraphFunction](GraphFunction.md) | None | 

