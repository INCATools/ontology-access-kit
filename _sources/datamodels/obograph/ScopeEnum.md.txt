# Enum: ScopeEnum




_A vocabulary of terms that can be used to "scope" a synonym_



URI: [ScopeEnum](ScopeEnum.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| hasExactSynonym | oio:hasExactSynonym | The synonym represents the exact meaning of the node |
| hasNarrowSynonym | oio:hasNarrowSynonym | The synonym represents something narrower in meaning than the node |
| hasBroadSynonym | oio:hasBroadSynonym | The synonym represents something broader in meaning than the node |
| hasRelatedSynonym | oio:hasRelatedSynonym | The synonym represents something closely related in meaning than the node, bu... |




## Slots

| Name | Description |
| ---  | --- |
| [pred](pred.md) |  |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs






## LinkML Source

<details>
```yaml
name: ScopeEnum
description: A vocabulary of terms that can be used to "scope" a synonym
from_schema: https://github.com/geneontology/obographs
rank: 1000
permissible_values:
  hasExactSynonym:
    text: hasExactSynonym
    description: The synonym represents the exact meaning of the node.
    meaning: oio:hasExactSynonym
  hasNarrowSynonym:
    text: hasNarrowSynonym
    description: The synonym represents something narrower in meaning than the node.
    meaning: oio:hasNarrowSynonym
  hasBroadSynonym:
    text: hasBroadSynonym
    description: The synonym represents something broader in meaning than the node.
    meaning: oio:hasBroadSynonym
  hasRelatedSynonym:
    text: hasRelatedSynonym
    description: The synonym represents something closely related in meaning than
      the node, but in not exact, broad, or narrow.
    meaning: oio:hasRelatedSynonym

```
</details>
