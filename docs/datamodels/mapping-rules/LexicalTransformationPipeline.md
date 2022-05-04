# Class: LexicalTransformationPipeline
_A collection of atomic lexical transformations that are applied in serial fashion_





URI: [li:LexicalTransformationPipeline](https://w3id.org/linkml/lexical_index/LexicalTransformationPipeline)




## Inheritance

* [Activity](Activity.md)
    * **LexicalTransformationPipeline**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [name](name.md) | [string](string.md) | 0..1 | None  | . |
| [transformations](transformations.md) | [LexicalTransformation](LexicalTransformation.md) | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalIndex](LexicalIndex.md) | [pipelines](pipelines.md) | range | LexicalTransformationPipeline |
| [RelationshipToTerm](RelationshipToTerm.md) | [pipeline](pipeline.md) | range | LexicalTransformationPipeline |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalTransformationPipeline
description: A collection of atomic lexical transformations that are applied in serial
  fashion
from_schema: https://w3id.org/linkml/lexical_index
is_a: Activity
attributes:
  name:
    name: name
    from_schema: https://w3id.org/linkml/lexical_index
    key: true
  transformations:
    name: transformations
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    range: LexicalTransformation

```
</details>

### Induced

<details>
```yaml
name: LexicalTransformationPipeline
description: A collection of atomic lexical transformations that are applied in serial
  fashion
from_schema: https://w3id.org/linkml/lexical_index
is_a: Activity
attributes:
  name:
    name: name
    from_schema: https://w3id.org/linkml/lexical_index
    key: true
    alias: name
    owner: LexicalTransformationPipeline
    range: string
  transformations:
    name: transformations
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    alias: transformations
    owner: LexicalTransformationPipeline
    range: LexicalTransformation

```
</details>