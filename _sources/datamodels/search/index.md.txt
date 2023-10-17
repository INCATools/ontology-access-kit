# search datamodel

A datamodel for representing a search configuration and results.

This is intended to provide a unified layer over both:

- (a) how searches are *parameterized*
- (b) the structure of search *results*.

The scope is any kind of service that provides search over *named entities*, including ontology concepts. It is not intended to cover generic
search results, e.g. google search, although parts could be generalized for this purpose.

URI: https://w3id.org/oak/search-datamodel

Name: search-datamodel



## Classes

| Class | Description |
| --- | --- |
| [ComplexQuery](ComplexQuery.md) | None |
| [PathExpression](PathExpression.md) | A path query |
| [SearchBaseConfiguration](SearchBaseConfiguration.md) | A user-specified configuration that determines how a particular search operation works |
| [SearchResult](SearchResult.md) | An individual search result |
| [SearchResultSet](SearchResultSet.md) | None |



## Slots

| Slot | Description |
| --- | --- |
| [all_of](all_of.md) |  |
| [any_of](any_of.md) |  |
| [atom](atom.md) |  |
| [categories](categories.md) | categories that should be matched |
| [configuration](configuration.md) |  |
| [cursor](cursor.md) | when the number of search results exceed the limit this can be used to iterat... |
| [force_case_insensitive](force_case_insensitive.md) | force case insensitive matching |
| [graph_predicates](graph_predicates.md) |  |
| [include_obsoletes_in_results](include_obsoletes_in_results.md) |  |
| [is_complete](is_complete.md) |  |
| [is_fuzzy](is_fuzzy.md) |  |
| [is_partial](is_partial.md) | allows matches where the search term is a subset of the full span |
| [limit](limit.md) | the maximum number of search results to be returned in one batch |
| [matches_full_search_term](matches_full_search_term.md) | Does the matched field match the full string |
| [none_of](none_of.md) |  |
| [object_id](object_id.md) | The CURIE of the matched term |
| [object_label](object_label.md) | The label/name of the matched term |
| [object_match_field](object_match_field.md) | The field/property in which the match was found |
| [object_source](object_source.md) | The ontology or other source that contains the matched term |
| [object_source_version](object_source_version.md) | Version IRI or version string of the source of the object term |
| [path_to](path_to.md) |  |
| [properties](properties.md) | determines which properties are searched over |
| [rank](rank.md) | For relevancy-ranked results, this indicates the relevancy, with low numbers ... |
| [result_count](result_count.md) |  |
| [results](results.md) |  |
| [search_term](search_term.md) |  |
| [search_terms](search_terms.md) | An individual search term |
| [snippet](snippet.md) | shows how the field was matched |
| [syntax](syntax.md) | Determines how the search term is interpreted |
| [traversal](traversal.md) |  |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [BooleanOperator](BooleanOperator.md) |  |
| [GraphFunction](GraphFunction.md) |  |
| [SearchProperty](SearchProperty.md) | A property that can be searched on |
| [SearchTermSyntax](SearchTermSyntax.md) |  |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [SearchTerm](SearchTerm.md) |  |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
