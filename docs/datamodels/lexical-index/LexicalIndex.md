

# Class: LexicalIndex


_An index over an ontology keyed by lexical unit_





URI: [ontolexindex:LexicalIndex](https://w3id.org/oak/lexical-index/LexicalIndex)






```{mermaid}
 classDiagram
    class LexicalIndex
    click LexicalIndex href "../LexicalIndex"
      LexicalIndex : groupings
        
          
    
    
    LexicalIndex --> "*" LexicalGrouping : groupings
    click LexicalGrouping href "../LexicalGrouping"

        
      LexicalIndex : pipelines
        
          
    
    
    LexicalIndex --> "*" LexicalTransformationPipeline : pipelines
    click LexicalTransformationPipeline href "../LexicalTransformationPipeline"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [groupings](groupings.md) | * <br/> [LexicalGrouping](LexicalGrouping.md) | all groupings | direct |
| [pipelines](pipelines.md) | * <br/> [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | all pipelines used to build the index | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/lexical-index




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontolexindex:LexicalIndex |
| native | ontolexindex:LexicalIndex |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalIndex
description: An index over an ontology keyed by lexical unit
from_schema: https://w3id.org/oak/lexical-index
attributes:
  groupings:
    name: groupings
    description: all groupings
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - LexicalIndex
    range: LexicalGrouping
    multivalued: true
    inlined: true
  pipelines:
    name: pipelines
    description: all pipelines used to build the index
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - LexicalIndex
    range: LexicalTransformationPipeline
    multivalued: true
    inlined: true

```
</details>

### Induced

<details>
```yaml
name: LexicalIndex
description: An index over an ontology keyed by lexical unit
from_schema: https://w3id.org/oak/lexical-index
attributes:
  groupings:
    name: groupings
    description: all groupings
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: groupings
    owner: LexicalIndex
    domain_of:
    - LexicalIndex
    range: LexicalGrouping
    multivalued: true
    inlined: true
  pipelines:
    name: pipelines
    description: all pipelines used to build the index
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: pipelines
    owner: LexicalIndex
    domain_of:
    - LexicalIndex
    range: LexicalTransformationPipeline
    multivalued: true
    inlined: true

```
</details>