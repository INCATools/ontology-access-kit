# Class: StructureDiffResultSet
_A collection of relational diff results_




URI: [ann:StructureDiffResultSet](https://w3id.org/linkml/text_annotator/StructureDiffResultSet)



```{mermaid}
 classDiagram
    class StructureDiffResultSet
      StructureDiffResultSet : left_source
      StructureDiffResultSet : results
      StructureDiffResultSet : right_source
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [results](results.md) | 0..* <br/> [RelationalDiff](RelationalDiff.md) | all differences between a pair of ontologies | direct |
| [left_source](left_source.md) | 0..1 <br/> [Source](Source.md) | Ontology source for left entities | direct |
| [right_source](right_source.md) | 0..1 <br/> [Source](Source.md) | Ontology source for right entities | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:StructureDiffResultSet |
| native | ann:StructureDiffResultSet |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: StructureDiffResultSet
description: A collection of relational diff results
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
attributes:
  results:
    name: results
    description: all differences between a pair of ontologies
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    multivalued: true
    range: RelationalDiff
    inlined: true
  left_source:
    name: left_source
    description: Ontology source for left entities
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    range: Source
  right_source:
    name: right_source
    description: Ontology source for right entities
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    range: Source

```
</details>

### Induced

<details>
```yaml
name: StructureDiffResultSet
description: A collection of relational diff results
from_schema: https://w3id.org/linkml/cross_ontology_diff
rank: 1000
attributes:
  results:
    name: results
    description: all differences between a pair of ontologies
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    multivalued: true
    alias: results
    owner: StructureDiffResultSet
    domain_of:
    - StructureDiffResultSet
    range: RelationalDiff
    inlined: true
  left_source:
    name: left_source
    description: Ontology source for left entities
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    alias: left_source
    owner: StructureDiffResultSet
    domain_of:
    - StructureDiffResultSet
    range: Source
  right_source:
    name: right_source
    description: Ontology source for right entities
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    rank: 1000
    alias: right_source
    owner: StructureDiffResultSet
    domain_of:
    - StructureDiffResultSet
    range: Source

```
</details>