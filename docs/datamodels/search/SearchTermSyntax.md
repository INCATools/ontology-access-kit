# Enum: SearchTermSyntax



URI: [SearchTermSyntax](SearchTermSyntax.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| PLAINTEXT | None | The search term is plain text with no special syntax |
| REGULAR_EXPRESSION | None | The search term is a regular expression, ECMAscript style assumed |
| SQL | None | The search term is SQL LIKE syntax, with percent symbols acting as wildcards |
| LUCENE | None | The search term is in Lucene/Solr syntax |
| STARTS_WITH | None | The search term is plain text but the matched field must start with the searc... |




## Slots

| Name | Description |
| ---  | --- |
| [syntax](syntax.md) | Determines how the search term is interpreted |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/search-datamodel






## LinkML Source

<details>
```yaml
name: SearchTermSyntax
from_schema: https://w3id.org/oak/search-datamodel
rank: 1000
permissible_values:
  PLAINTEXT:
    text: PLAINTEXT
    description: The search term is plain text with no special syntax
  REGULAR_EXPRESSION:
    text: REGULAR_EXPRESSION
    description: The search term is a regular expression, ECMAscript style assumed
  SQL:
    text: SQL
    description: The search term is SQL LIKE syntax, with percent symbols acting as
      wildcards
  LUCENE:
    text: LUCENE
    description: The search term is in Lucene/Solr syntax
  STARTS_WITH:
    text: STARTS_WITH
    description: The search term is plain text but the matched field must start with
      the search term

```
</details>
