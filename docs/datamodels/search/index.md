# search datamodel

A datamodel for representing a search configuration and results. This is intended to provide a unified layer over both (a) how searches are *parameterized* (b) the structure of search *results*. The scope is any kind of service that provides search over *named entities*, including ontology concepts. It is not intended to cover generic search results, e.g. google search, although parts could be generalized for this purpose.

URI: https://w3id.org/linkml/search_datamodel
Name: search-datamodel

## Classes

| Class | Description |
| --- | --- |
| [AtomicQuery](AtomicQuery.md) | None |
| [BooleanQuery](BooleanQuery.md) | None |
| [SearchBaseConfiguration](SearchBaseConfiguration.md) | A user-specified configuration that determines how a particular search operation works |
| [SearchResult](SearchResult.md) | An individual search result |
| [SearchResultSet](SearchResultSet.md) | None |


## Slots

| Slot | Description |
| --- | --- |
| [atom](atom.md) | None |
| [categories](categories.md) | None |
| [configuration](configuration.md) | None |
| [cursor](cursor.md) | when the number of search results exceed the limit this can be used to iterate through results |
| [graph_function](graph_function.md) | None |
| [graph_predicates](graph_predicates.md) | None |
| [include_aliases](include_aliases.md) | None |
| [include_definition](include_definition.md) | None |
| [include_id](include_id.md) | None |
| [include_label](include_label.md) | None |
| [include_obsoletes_in_results](include_obsoletes_in_results.md) | None |
| [is_complete](is_complete.md) | restricts search results to matches of the full span of the string |
| [is_partial](is_partial.md) | None |
| [is_regular_expression](is_regular_expression.md) | None |
| [limit](limit.md) | the maximum number of search results to be returned in one batch |
| [matches_full_search_term](matches_full_search_term.md) | Does the matched field match the full string |
| [object_id](object_id.md) | The CURIE of the matched term |
| [object_label](object_label.md) | The label/name of the matched term |
| [object_match_field](object_match_field.md) | The field/property in which the match was found |
| [object_source](object_source.md) | The ontology or other source that contains the matched term |
| [object_source_version](object_source_version.md) | Version IRI or version string of the source of the object term. |
| [operands](operands.md) | None |
| [operator](operator.md) | None |
| [properties](properties.md) | determines which properties are searched over |
| [rank](rank.md) | For relevancy-ranked results, this indicates the relevancy, with low numbers being the most relevant |
| [result_count](result_count.md) | None |
| [results](results.md) | None |
| [search_term](search_term.md) | None |
| [search_terms](search_terms.md) | An individual search term. The syntax is determined by the syntax slot |
| [snippet](snippet.md) | shows how the field was matched |
| [syntax](syntax.md) | Determines how the search term is interpreted |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [BooleanOperator](BooleanOperator.md) | None |
| [GraphFunction](GraphFunction.md) | None |
| [SearchProperty](SearchProperty.md) | A property that can be searched on |
| [SearchTermSyntax](SearchTermSyntax.md) | None |


## Subsets

| Subset | Description |
| --- | --- |
