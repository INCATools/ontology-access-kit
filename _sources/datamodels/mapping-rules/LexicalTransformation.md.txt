# Class: LexicalTransformation
_An atomic lexical transformation applied on a term (string) yielding a transformed string_





URI: [li:LexicalTransformation](https://w3id.org/linkml/lexical_index/LexicalTransformation)




## Inheritance

* [Activity](Activity.md)
    * **LexicalTransformation**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [type](type.md) | [TransformationType](TransformationType.md) | 0..1 | The type of transformation  | . |
| [params](params.md) | [string](string.md) | 0..1 | Any parameters to be applied to the transformation algorithm  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | [transformations](transformations.md) | range | LexicalTransformation |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalTransformation
description: An atomic lexical transformation applied on a term (string) yielding
  a transformed string
from_schema: https://w3id.org/linkml/lexical_index
is_a: Activity
attributes:
  type:
    name: type
    description: The type of transformation
    from_schema: https://w3id.org/linkml/lexical_index
    range: TransformationType
  params:
    name: params
    description: Any parameters to be applied to the transformation algorithm
    from_schema: https://w3id.org/linkml/lexical_index

```
</details>

### Induced

<details>
```yaml
name: LexicalTransformation
description: An atomic lexical transformation applied on a term (string) yielding
  a transformed string
from_schema: https://w3id.org/linkml/lexical_index
is_a: Activity
attributes:
  type:
    name: type
    description: The type of transformation
    from_schema: https://w3id.org/linkml/lexical_index
    alias: type
    owner: LexicalTransformation
    range: TransformationType
  params:
    name: params
    description: Any parameters to be applied to the transformation algorithm
    from_schema: https://w3id.org/linkml/lexical_index
    alias: params
    owner: LexicalTransformation
    range: string

```
</details>