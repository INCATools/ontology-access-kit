# Class: LexicalTransformationPipeline
_A collection of atomic lexical transformations that are applied in serial fashion_




URI: [li:LexicalTransformationPipeline](https://w3id.org/linkml/lexical_index/LexicalTransformationPipeline)



```{mermaid}
 classDiagram
    class LexicalTransformationPipeline
      Activity <|-- LexicalTransformationPipeline
      
      LexicalTransformationPipeline : name
      LexicalTransformationPipeline : transformations
      
```





## Inheritance
* [Activity](Activity.md)
    * **LexicalTransformationPipeline**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [name](name.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [transformations](transformations.md) | 0..* <br/> [LexicalTransformation](LexicalTransformation.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalIndex](LexicalIndex.md) | [pipelines](pipelines.md) | range | [LexicalTransformationPipeline](LexicalTransformationPipeline.md) |
| [RelationshipToTerm](RelationshipToTerm.md) | [pipeline](pipeline.md) | range | [LexicalTransformationPipeline](LexicalTransformationPipeline.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/lexical_index





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | li:LexicalTransformationPipeline |
| native | li:LexicalTransformationPipeline |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalTransformationPipeline
description: A collection of atomic lexical transformations that are applied in serial
  fashion
from_schema: https://w3id.org/linkml/lexical_index
rank: 1000
is_a: Activity
attributes:
  name:
    name: name
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    key: true
  transformations:
    name: transformations
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
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
rank: 1000
is_a: Activity
attributes:
  name:
    name: name
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    key: true
    alias: name
    owner: LexicalTransformationPipeline
    domain_of:
    - LexicalTransformationPipeline
    range: string
  transformations:
    name: transformations
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    multivalued: true
    alias: transformations
    owner: LexicalTransformationPipeline
    domain_of:
    - LexicalTransformationPipeline
    range: LexicalTransformation

```
</details>