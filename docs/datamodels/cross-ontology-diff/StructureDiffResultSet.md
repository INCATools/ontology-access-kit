# Class: StructureDiffResultSet
_A collection of results_





URI: [ann:StructureDiffResultSet](https://w3id.org/linkml/text_annotator/StructureDiffResultSet)




```{mermaid}
 classDiagram
    class StructureDiffResultSet
      StructureDiffResultSet : results
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [results](results.md) | [RelationalDiff](RelationalDiff.md) | 0..* | all annotations  | . |


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
description: A collection of results
from_schema: https://w3id.org/linkml/cross_ontology_diff
attributes:
  results:
    name: results
    description: all annotations
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    multivalued: true
    range: RelationalDiff
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: StructureDiffResultSet
description: A collection of results
from_schema: https://w3id.org/linkml/cross_ontology_diff
attributes:
  results:
    name: results
    description: all annotations
    from_schema: https://w3id.org/linkml/cross_ontology_diff
    multivalued: true
    alias: results
    owner: StructureDiffResultSet
    range: RelationalDiff
    inlined: true

```
</details>