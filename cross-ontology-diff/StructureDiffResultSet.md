# Class: StructureDiffResultSet
_A collection of results_





URI: [ann:StructureDiffResultSet](https://w3id.org/linkml/text_annotator/StructureDiffResultSet)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [results](results.md) | [RelationalDiff](RelationalDiff.md) | 0..* | all annotations  | . |


## Usages



## Identifier and Mapping Information









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
    inlined: true
    range: RelationalDiff

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
    inlined: true
    alias: results
    owner: StructureDiffResultSet
    range: RelationalDiff

```
</details>