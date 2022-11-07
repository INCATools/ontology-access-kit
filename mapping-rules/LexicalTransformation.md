# Class: LexicalTransformation
_An atomic lexical transformation applied on a term (string) yielding a transformed string_




URI: [li:LexicalTransformation](https://w3id.org/linkml/lexical_index/LexicalTransformation)


```{mermaid}
 classDiagram
    class LexicalTransformation
      Activity <|-- LexicalTransformation
      
      LexicalTransformation : params
      LexicalTransformation : type
      
```




## Inheritance
* [Activity](Activity.md)
    * **LexicalTransformation**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [type](type.md) | 0..1 <br/> TransformationType | The type of transformation | direct |
| [params](params.md) | 0..1 <br/> None | Any parameters to be applied to the transformation algorithm | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | [transformations](transformations.md) | range | LexicalTransformation |







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/lexical_index





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | li:LexicalTransformation |
| native | li:LexicalTransformation |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalTransformation
description: An atomic lexical transformation applied on a term (string) yielding
  a transformed string
from_schema: https://w3id.org/linkml/lexical_index
rank: 1000
is_a: Activity
attributes:
  type:
    name: type
    description: The type of transformation
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    range: TransformationType
  params:
    name: params
    description: Any parameters to be applied to the transformation algorithm
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000

```
</details>

### Induced

<details>
```yaml
name: LexicalTransformation
description: An atomic lexical transformation applied on a term (string) yielding
  a transformed string
from_schema: https://w3id.org/linkml/lexical_index
rank: 1000
is_a: Activity
attributes:
  type:
    name: type
    description: The type of transformation
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    alias: type
    owner: LexicalTransformation
    domain_of:
    - LexicalTransformation
    range: TransformationType
  params:
    name: params
    description: Any parameters to be applied to the transformation algorithm
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    alias: params
    owner: LexicalTransformation
    domain_of:
    - LexicalTransformation
    range: string

```
</details>