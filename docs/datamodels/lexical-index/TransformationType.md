# Enum: TransformationType




_A controlled datamodels of the types of transformation that can be applied to_



URI: [TransformationType](TransformationType.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Stemming | None | Removal of the last few characters of a word to yield a stem term for each wo... |
| Lemmatization | None | Contextual reduction of a word to its base form for each word in the term |
| WordOrderNormalization | None | reorder words in the term to a standard order such that comparisons are order... |
| Depluralization | None | Transform plural form to singular form for each word in a term |
| CaseNormalization | None | Transform term to a standard case, typically lowercase |
| WhitespaceNormalization | None | Trim whitespace, condense whitespace runs, and transform all non-space whites... |
| TermExpanson | None | Expand terms using a dictionary |
| Synonymization | None | Applying synonymizer rules from matcher_rules |




## Slots

| Name | Description |
| ---  | --- |
| [type](type.md) | The type of transformation |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/lexical-index






## LinkML Source

<details>
```yaml
name: TransformationType
description: A controlled datamodels of the types of transformation that can be applied
  to
from_schema: https://w3id.org/oak/lexical-index
rank: 1000
permissible_values:
  Stemming:
    text: Stemming
    description: Removal of the last few characters of a word to yield a stem term
      for each word in the term
  Lemmatization:
    text: Lemmatization
    description: Contextual reduction of a word to its base form for each word in
      the term
  WordOrderNormalization:
    text: WordOrderNormalization
    description: reorder words in the term to a standard order such that comparisons
      are order-independent
  Depluralization:
    text: Depluralization
    description: Transform plural form to singular form for each word in a term
  CaseNormalization:
    text: CaseNormalization
    description: Transform term to a standard case, typically lowercase
  WhitespaceNormalization:
    text: WhitespaceNormalization
    description: Trim whitespace, condense whitespace runs, and transform all non-space
      whitespace to spaces
  TermExpanson:
    text: TermExpanson
    description: Expand terms using a dictionary
  Synonymization:
    text: Synonymization
    description: Applying synonymizer rules from matcher_rules.yaml

```
</details>
