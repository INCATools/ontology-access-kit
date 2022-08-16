# Class: TermPairwiseSimilarity
_A simple pairwise similarity between two atomic concepts/terms_





URI: [sim:TermPairwiseSimilarity](https://w3id.org/linkml/similarity/TermPairwiseSimilarity)




```{mermaid}
 classDiagram
      PairwiseSimilarity <|-- TermPairwiseSimilarity
      
      TermPairwiseSimilarity : ancestor_id
      TermPairwiseSimilarity : ancestor_information_content
      TermPairwiseSimilarity : ancestor_label
      TermPairwiseSimilarity : ancestor_source
      TermPairwiseSimilarity : dice_similarity
      TermPairwiseSimilarity : jaccard_similarity
      TermPairwiseSimilarity : object_id
      TermPairwiseSimilarity : object_information_content
      TermPairwiseSimilarity : object_label
      TermPairwiseSimilarity : object_source
      TermPairwiseSimilarity : phenodigm_score
      TermPairwiseSimilarity : subject_id
      TermPairwiseSimilarity : subject_information_content
      TermPairwiseSimilarity : subject_label
      TermPairwiseSimilarity : subject_source
      

```





## Inheritance
* [PairwiseSimilarity](PairwiseSimilarity.md)
    * **TermPairwiseSimilarity**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [subject_id](subject_id.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 1..1 | The first of the two entities being compared  | . |
| [subject_label](subject_label.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | the label or name for the first entity  | . |
| [subject_source](subject_source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | the source for the first entity  | . |
| [object_id](object_id.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..1 | The second of the two entities being compared  | . |
| [object_label](object_label.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | the label or name for the second entity  | . |
| [object_source](object_source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | the source for the second entity  | . |
| [ancestor_id](ancestor_id.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..1 | the most recent common ancestor of the two compared entities. If there are multiple MRCAs then the most informative one is selected  | . |
| [ancestor_label](ancestor_label.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | the name or label of the ancestor concept  | . |
| [ancestor_source](ancestor_source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [object_information_content](object_information_content.md) | [NegativeLogValue](NegativeLogValue.md) | 0..1 | The IC of the object  | . |
| [subject_information_content](subject_information_content.md) | [NegativeLogValue](NegativeLogValue.md) | 0..1 | The IC of the subject  | . |
| [ancestor_information_content](ancestor_information_content.md) | [NegativeLogValue](NegativeLogValue.md) | 0..1 | The IC of the object  | . |
| [jaccard_similarity](jaccard_similarity.md) | [ZeroToOne](ZeroToOne.md) | 0..1 | The number of concepts in the intersection divided by the number in the union  | . |
| [dice_similarity](dice_similarity.md) | [ZeroToOne](ZeroToOne.md) | 0..1 | None  | . |
| [phenodigm_score](phenodigm_score.md) | [NonNegativeFloat](NonNegativeFloat.md) | 0..1 | the geometric mean of the jaccard similarity and the information content  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/similarity







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['sim:TermPairwiseSimilarity'] |
| native | ['sim:TermPairwiseSimilarity'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TermPairwiseSimilarity
description: A simple pairwise similarity between two atomic concepts/terms
from_schema: https://w3id.org/linkml/similarity
is_a: PairwiseSimilarity

```
</details>

### Induced

<details>
```yaml
name: TermPairwiseSimilarity
description: A simple pairwise similarity between two atomic concepts/terms
from_schema: https://w3id.org/linkml/similarity
is_a: PairwiseSimilarity
attributes:
  subject_id:
    name: subject_id
    description: The first of the two entities being compared
    from_schema: https://w3id.org/linkml/similarity
    slot_uri: sssom:subject_id
    alias: subject_id
    owner: TermPairwiseSimilarity
    range: uriorcurie
    required: true
  subject_label:
    name: subject_label
    description: the label or name for the first entity
    from_schema: https://w3id.org/linkml/similarity
    slot_uri: sssom:subject_label
    alias: subject_label
    owner: TermPairwiseSimilarity
    range: string
  subject_source:
    name: subject_source
    description: the source for the first entity
    from_schema: https://w3id.org/linkml/similarity
    slot_uri: sssom:subject_source
    alias: subject_source
    owner: TermPairwiseSimilarity
    range: string
  object_id:
    name: object_id
    description: The second of the two entities being compared
    from_schema: https://w3id.org/linkml/similarity
    slot_uri: sssom:object_id
    alias: object_id
    owner: TermPairwiseSimilarity
    range: uriorcurie
  object_label:
    name: object_label
    description: the label or name for the second entity
    from_schema: https://w3id.org/linkml/similarity
    slot_uri: sssom:object_label
    alias: object_label
    owner: TermPairwiseSimilarity
    range: string
  object_source:
    name: object_source
    description: the source for the second entity
    from_schema: https://w3id.org/linkml/similarity
    slot_uri: sssom:object_source
    alias: object_source
    owner: TermPairwiseSimilarity
    range: string
  ancestor_id:
    name: ancestor_id
    description: the most recent common ancestor of the two compared entities. If
      there are multiple MRCAs then the most informative one is selected
    todos:
    - decide on what to do when there are multiple possible ancestos
    from_schema: https://w3id.org/linkml/similarity
    alias: ancestor_id
    owner: TermPairwiseSimilarity
    range: uriorcurie
  ancestor_label:
    name: ancestor_label
    description: the name or label of the ancestor concept
    from_schema: https://w3id.org/linkml/similarity
    alias: ancestor_label
    owner: TermPairwiseSimilarity
    range: string
  ancestor_source:
    name: ancestor_source
    from_schema: https://w3id.org/linkml/similarity
    alias: ancestor_source
    owner: TermPairwiseSimilarity
    range: string
  object_information_content:
    name: object_information_content
    description: The IC of the object
    from_schema: https://w3id.org/linkml/similarity
    is_a: information_content
    alias: object_information_content
    owner: TermPairwiseSimilarity
    range: NegativeLogValue
  subject_information_content:
    name: subject_information_content
    description: The IC of the subject
    from_schema: https://w3id.org/linkml/similarity
    is_a: information_content
    alias: subject_information_content
    owner: TermPairwiseSimilarity
    range: NegativeLogValue
  ancestor_information_content:
    name: ancestor_information_content
    description: The IC of the object
    from_schema: https://w3id.org/linkml/similarity
    is_a: information_content
    alias: ancestor_information_content
    owner: TermPairwiseSimilarity
    range: NegativeLogValue
  jaccard_similarity:
    name: jaccard_similarity
    description: The number of concepts in the intersection divided by the number
      in the union
    from_schema: https://w3id.org/linkml/similarity
    is_a: score
    alias: jaccard_similarity
    owner: TermPairwiseSimilarity
    range: ZeroToOne
  dice_similarity:
    name: dice_similarity
    from_schema: https://w3id.org/linkml/similarity
    is_a: score
    alias: dice_similarity
    owner: TermPairwiseSimilarity
    range: ZeroToOne
  phenodigm_score:
    name: phenodigm_score
    description: the geometric mean of the jaccard similarity and the information
      content
    from_schema: https://w3id.org/linkml/similarity
    is_a: score
    alias: phenodigm_score
    owner: TermPairwiseSimilarity
    range: NonNegativeFloat
    equals_expression: sqrt({jaccard_similarity} * {information_content})

```
</details>