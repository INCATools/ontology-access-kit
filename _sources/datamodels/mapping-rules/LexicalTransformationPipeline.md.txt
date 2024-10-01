

# Class: LexicalTransformationPipeline


_A collection of atomic lexical transformations that are applied in serial fashion_





URI: [mappingrules:LexicalTransformationPipeline](https://w3id.org/oak/mapping-rules-datamodel/LexicalTransformationPipeline)






```{mermaid}
 classDiagram
    class LexicalTransformationPipeline
    click LexicalTransformationPipeline href "../LexicalTransformationPipeline"
      Activity <|-- LexicalTransformationPipeline
        click Activity href "../Activity"
      
      LexicalTransformationPipeline : name
        
      LexicalTransformationPipeline : transformations
        
          
    
    
    LexicalTransformationPipeline --> "*" LexicalTransformation : transformations
    click LexicalTransformation href "../LexicalTransformation"

        
      
```





## Inheritance
* [Activity](Activity.md)
    * **LexicalTransformationPipeline**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [name](name.md) | 0..1 <br/> [String](String.md) |  | direct |
| [transformations](transformations.md) | * <br/> [LexicalTransformation](LexicalTransformation.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalIndex](LexicalIndex.md) | [pipelines](pipelines.md) | range | [LexicalTransformationPipeline](LexicalTransformationPipeline.md) |
| [RelationshipToTerm](RelationshipToTerm.md) | [pipeline](pipeline.md) | range | [LexicalTransformationPipeline](LexicalTransformationPipeline.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:LexicalTransformationPipeline |
| native | mappingrules:LexicalTransformationPipeline |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalTransformationPipeline
description: A collection of atomic lexical transformations that are applied in serial
  fashion
from_schema: https://w3id.org/oak/mapping-rules-datamodel
is_a: Activity
attributes:
  name:
    name: name
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    key: true
    domain_of:
    - LexicalTransformationPipeline
    required: true
  transformations:
    name: transformations
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - LexicalTransformationPipeline
    range: LexicalTransformation
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: LexicalTransformationPipeline
description: A collection of atomic lexical transformations that are applied in serial
  fashion
from_schema: https://w3id.org/oak/mapping-rules-datamodel
is_a: Activity
attributes:
  name:
    name: name
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    key: true
    alias: name
    owner: LexicalTransformationPipeline
    domain_of:
    - LexicalTransformationPipeline
    range: string
    required: true
  transformations:
    name: transformations
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: transformations
    owner: LexicalTransformationPipeline
    domain_of:
    - LexicalTransformationPipeline
    range: LexicalTransformation
    multivalued: true

```
</details>