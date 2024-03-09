# Class: LexicalIndex


_An index over an ontology keyed by lexical unit_





URI: [mappingrules:LexicalIndex](https://w3id.org/oak/mapping-rules-datamodel/LexicalIndex)




```{mermaid}
 classDiagram
    class LexicalIndex
      LexicalIndex : groupings
        
          LexicalIndex --> LexicalGrouping : groupings
        
      LexicalIndex : pipelines
        
          LexicalIndex --> LexicalTransformationPipeline : pipelines
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [groupings](groupings.md) | 0..* <br/> [LexicalGrouping](LexicalGrouping.md) | all groupings | direct |
| [pipelines](pipelines.md) | 0..* <br/> [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | all pipelines used to build the index | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:LexicalIndex |
| native | mappingrules:LexicalIndex |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalIndex
description: An index over an ontology keyed by lexical unit
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  groupings:
    name: groupings
    description: all groupings
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    multivalued: true
    domain_of:
    - LexicalIndex
    range: LexicalGrouping
    inlined: true
  pipelines:
    name: pipelines
    description: all pipelines used to build the index
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    multivalued: true
    domain_of:
    - LexicalIndex
    range: LexicalTransformationPipeline
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: LexicalIndex
description: An index over an ontology keyed by lexical unit
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  groupings:
    name: groupings
    description: all groupings
    from_schema: https://w3id.org/oak/lexical-index
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
    from_schema: https://w3id.org/oak/lexical-index
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