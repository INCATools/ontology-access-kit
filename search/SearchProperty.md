# Enum: SearchProperty




_A property that can be searched on_



URI: [SearchProperty](SearchProperty.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| IDENTIFIER | schema:identifier | The identifier or URI of the entity |
| REPLACEMENT_IDENTIFIER | schema:identifier | A replacement identifier or URI for the entity |
| MAPPED_IDENTIFIER | skos:closeMatch | An identifier or URI for a mapping |
| LABEL | rdfs:label | The preferred label / human readable name of the entity |
| ALIAS | skos:altLabel | An alias or synonym of the entity |
| COMMENT | rdfs:comment | A comment on the entity |
| DEFINITION | skos:definition | The definition of the entity |
| INFORMATIVE_TEXT | None | Any informative text attached to the entity including comments, definitions, ... |
| ANYTHING | rdf:Property |  |




## Slots

| Name | Description |
| ---  | --- |
| [properties](properties.md) | determines which properties are searched over |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/search-datamodel






## LinkML Source

<details>
```yaml
name: SearchProperty
description: A property that can be searched on
from_schema: https://w3id.org/oak/search-datamodel
rank: 1000
permissible_values:
  IDENTIFIER:
    text: IDENTIFIER
    description: The identifier or URI of the entity
    meaning: schema:identifier
  REPLACEMENT_IDENTIFIER:
    text: REPLACEMENT_IDENTIFIER
    description: A replacement identifier or URI for the entity
    meaning: schema:identifier
  MAPPED_IDENTIFIER:
    text: MAPPED_IDENTIFIER
    description: An identifier or URI for a mapping
    meaning: skos:closeMatch
  LABEL:
    text: LABEL
    description: The preferred label / human readable name of the entity
    meaning: rdfs:label
  ALIAS:
    text: ALIAS
    description: An alias or synonym of the entity
    meaning: skos:altLabel
  COMMENT:
    text: COMMENT
    description: A comment on the entity
    meaning: rdfs:comment
  DEFINITION:
    text: DEFINITION
    description: The definition of the entity
    meaning: skos:definition
  INFORMATIVE_TEXT:
    text: INFORMATIVE_TEXT
    description: Any informative text attached to the entity including comments, definitions,
      descriptions, examples
  ANYTHING:
    text: ANYTHING
    meaning: rdf:Property

```
</details>
