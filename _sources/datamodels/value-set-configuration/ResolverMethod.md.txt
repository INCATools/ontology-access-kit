# Enum: ResolverMethod



URI: [ResolverMethod](ResolverMethod.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| SemanticSQL | None |  |
| OLS | None |  |
| BioPortal | None |  |
| OntoBee | None |  |
| Ubergraph | None |  |
| TCCM | None |  |
| SPARQL | None |  |
| LOV | None |  |
| Pronto | None |  |
| Uniprot | None |  |




## Slots

| Name | Description |
| ---  | --- |
| [method](method.md) | The method used to resolve the value set |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/value-set-configuration






## LinkML Source

<details>
```yaml
name: ResolverMethod
from_schema: https://w3id.org/linkml/value-set-configuration
rank: 1000
permissible_values:
  SemanticSQL:
    text: SemanticSQL
    annotations:
      prefix:
        tag: prefix
        value: sqlite:obo
  OLS:
    text: OLS
    annotations:
      prefix:
        tag: prefix
        value: ols
  BioPortal:
    text: BioPortal
    annotations:
      prefix:
        tag: prefix
        value: bioportal
  OntoBee:
    text: OntoBee
    annotations:
      prefix:
        tag: prefix
        value: ontobee
  Ubergraph:
    text: Ubergraph
    annotations:
      prefix:
        tag: prefix
        value: ubergraph
  TCCM:
    text: TCCM
  SPARQL:
    text: SPARQL
  LOV:
    text: LOV
    annotations:
      prefix:
        tag: prefix
        value: lov
  Pronto:
    text: Pronto
    annotations:
      prefix:
        tag: prefix
        value: pronto
  Uniprot:
    text: Uniprot
    annotations:
      prefix:
        tag: prefix
        value: uniprot

```
</details>
