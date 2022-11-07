# Enum: MappingCardinalityEnum



URI: [MappingCardinalityEnum](MappingCardinalityEnum)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| 1:1 | None | One-to-one mapping |
| 1:n | None | One-to-many mapping |
| n:1 | None | Many-to-one mapping |
| 1:0 | None | One-to-none mapping |
| 0:1 | None | None-to-one mapping |
| n:n | None | Many-to-many mapping |







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff




## LinkML Source

<details>
```yaml
name: MappingCardinalityEnum
from_schema: https://w3id.org/linkml/cross_ontology_diff
exact_mappings:
- sssom:mapping_cardinality_enum
rank: 1000
permissible_values:
  '1:1':
    text: '1:1'
    description: One-to-one mapping
  1:n:
    text: 1:n
    description: One-to-many mapping
  n:1:
    text: n:1
    description: Many-to-one mapping
  '1:0':
    text: '1:0'
    description: One-to-none mapping
  0:1:
    text: 0:1
    description: None-to-one mapping
  n:n:
    text: n:n
    description: Many-to-many mapping

```
</details>
