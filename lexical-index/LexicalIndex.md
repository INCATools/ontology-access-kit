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

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [groupings](groupings.md) | 0..* <br/> [LexicalGrouping](LexicalGrouping.md) | all groupings | direct |
| [pipelines](pipelines.md) | 0..* <br/> [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | all pipelines used to build the index | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/lexical_index





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | li:LexicalIndex |
| native | li:LexicalIndex |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalIndex
description: An index over an ontology keyed by lexical unit
from_schema: https://w3id.org/linkml/lexical_index
rank: 1000
attributes:
  groupings:
    name: groupings
    description: all groupings
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    multivalued: true
    range: LexicalGrouping
    inlined: true
  pipelines:
    name: pipelines
    description: all pipelines used to build the index
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
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
rank: 1000
attributes:
  groupings:
    name: groupings
    description: all groupings
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    multivalued: true
    alias: groupings
    owner: LexicalIndex
    domain_of:
    - LexicalIndex
    range: LexicalGrouping
    inlined: true
  pipelines:
    name: pipelines
    description: all pipelines used to build the index
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    multivalued: true
    alias: pipelines
    owner: LexicalIndex
    domain_of:
    - LexicalIndex
    range: LexicalTransformationPipeline
    inlined: true

```
</details>