# Class: LexicalIndex
_An index over an ontology keyed by lexical unit_





URI: [li:LexicalIndex](https://w3id.org/linkml/lexical_index/LexicalIndex)




```{mermaid}
 classDiagram
    class LexicalIndex
      LexicalIndex : groupings
      LexicalIndex : pipelines
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [groupings](groupings.md) | [LexicalGrouping](LexicalGrouping.md) | 0..* | all groupings  | . |
| [pipelines](pipelines.md) | [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | 0..* | all pipelines used to build the index  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/lexical_index







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['li:LexicalIndex'] |
| native | ['li:LexicalIndex'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalIndex
description: An index over an ontology keyed by lexical unit
from_schema: https://w3id.org/linkml/lexical_index
attributes:
  groupings:
    name: groupings
    description: all groupings
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    range: LexicalGrouping
    inlined: true
  pipelines:
    name: pipelines
    description: all pipelines used to build the index
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    range: LexicalTransformationPipeline
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: LexicalIndex
description: An index over an ontology keyed by lexical unit
from_schema: https://w3id.org/linkml/lexical_index
attributes:
  groupings:
    name: groupings
    description: all groupings
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    alias: groupings
    owner: LexicalIndex
    range: LexicalGrouping
    inlined: true
  pipelines:
    name: pipelines
    description: all pipelines used to build the index
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    alias: pipelines
    owner: LexicalIndex
    range: LexicalTransformationPipeline
    inlined: true

```
</details>