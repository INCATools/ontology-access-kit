# Enum: InformationContentCorpusEnum



URI: [InformationContentCorpusEnum](InformationContentCorpusEnum.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| ontology | None | Term frequency is the number of terms in the ontology that are descendants of... |
| associations | None | Term frequency is the number of entities annotated to the term or any of its ... |




## Slots

| Name | Description |
| ---  | --- |
| [corpus](corpus.md) | The corpus used to determine term frequencies |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity






## LinkML Source

<details>
```yaml
name: InformationContentCorpusEnum
from_schema: https://w3id.org/oak/similarity
rank: 1000
permissible_values:
  ontology:
    text: ontology
    description: Term frequency is the number of terms in the ontology that are descendants
      of the term (reflexive, using the closure predicates)
  associations:
    text: associations
    description: Term frequency is the number of entities annotated to the term or
      any of its descendants (using the closure predicates)

```
</details>
