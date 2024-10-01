

# Class: LexicalTransformation


_An atomic lexical transformation applied on a term (string) yielding a transformed string_





URI: [ontolexindex:LexicalTransformation](https://w3id.org/oak/lexical-index/LexicalTransformation)






```{mermaid}
 classDiagram
    class LexicalTransformation
    click LexicalTransformation href "../LexicalTransformation"
      Activity <|-- LexicalTransformation
        click Activity href "../Activity"
      
      LexicalTransformation : params
        
          
    
    
    LexicalTransformation --> "*" Any : params
    click Any href "../Any"

        
      LexicalTransformation : type
        
          
    
    
    LexicalTransformation --> "0..1" TransformationType : type
    click TransformationType href "../TransformationType"

        
      
```





## Inheritance
* [Activity](Activity.md)
    * **LexicalTransformation**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [type](type.md) | 0..1 <br/> [TransformationType](TransformationType.md) | The type of transformation | direct |
| [params](params.md) | * <br/> [Any](Any.md) | Any parameters to be applied to the transformation algorithm | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | [transformations](transformations.md) | range | [LexicalTransformation](LexicalTransformation.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/lexical-index




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontolexindex:LexicalTransformation |
| native | ontolexindex:LexicalTransformation |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalTransformation
description: An atomic lexical transformation applied on a term (string) yielding
  a transformed string
from_schema: https://w3id.org/oak/lexical-index
is_a: Activity
attributes:
  type:
    name: type
    description: The type of transformation
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - LexicalTransformation
    range: TransformationType
  params:
    name: params
    description: Any parameters to be applied to the transformation algorithm
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - LexicalTransformation
    range: Any
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>

### Induced

<details>
```yaml
name: LexicalTransformation
description: An atomic lexical transformation applied on a term (string) yielding
  a transformed string
from_schema: https://w3id.org/oak/lexical-index
is_a: Activity
attributes:
  type:
    name: type
    description: The type of transformation
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: type
    owner: LexicalTransformation
    domain_of:
    - LexicalTransformation
    range: TransformationType
  params:
    name: params
    description: Any parameters to be applied to the transformation algorithm
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: params
    owner: LexicalTransformation
    domain_of:
    - LexicalTransformation
    range: Any
    multivalued: true
    inlined: true
    inlined_as_list: true

```
</details>