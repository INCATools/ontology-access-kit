# Class: StructureDiffResultSet
_A collection of relational diff results results_





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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [results](results.md) | [RelationalDiff](RelationalDiff.md) | 0..* | all differences between a pair of ontologies  | . |
| [left_source](left_source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [right_source](right_source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/cross_ontology_diff







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ann:StructureDiffResultSet'] |
| native | ['ann:StructureDiffResultSet'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: StructureDiffResultSet
description: A collection of relational diff results results
from_schema: https://w3id.org/linkml/cross_ontology_diff
attributes:
  results:
    name: results
    description: all differences between a pair of ontologies
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    multivalued: true
    range: RelationalDiff
    inlined: true
  left_source:
    name: left_source
    from_schema: https://w3id.org/linkml/cross_ontology_diff
  right_source:
    name: right_source
    from_schema: https://w3id.org/linkml/cross_ontology_diff

```
</details>

### Induced

<details>
```yaml
name: StructureDiffResultSet
description: A collection of relational diff results results
from_schema: https://w3id.org/linkml/cross_ontology_diff
attributes:
  results:
    name: results
    description: all differences between a pair of ontologies
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    multivalued: true
    alias: results
    owner: StructureDiffResultSet
    range: RelationalDiff
    inlined: true
  left_source:
    name: left_source
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: left_source
    owner: StructureDiffResultSet
    range: string
  right_source:
    name: right_source
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    alias: right_source
    owner: StructureDiffResultSet
    range: string

```
</details>