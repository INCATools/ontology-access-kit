# Class: PairwiseSimilarity
_Abstract grouping for representing individual pairwise similarities_



* __NOTE__: this is an abstract class and should not be instantiated directly



URI: [sim:PairwiseSimilarity](https://w3id.org/linkml/similarity/PairwiseSimilarity)




```{mermaid}
 classDiagram
      PairwiseSimilarity <|-- TermPairwiseSimilarity
      PairwiseSimilarity <|-- TermSetPairwiseSimilarity
      
      PairwiseSimilarity : ancestor_id
      PairwiseSimilarity : ancestor_information_content
      PairwiseSimilarity : ancestor_label
      PairwiseSimilarity : ancestor_source
      PairwiseSimilarity : dice_similarity
      PairwiseSimilarity : jaccard_similarity
      PairwiseSimilarity : object_id
      PairwiseSimilarity : object_information_content
      PairwiseSimilarity : object_label
      PairwiseSimilarity : object_source
      PairwiseSimilarity : phenodigm_score
      PairwiseSimilarity : subject_id
      PairwiseSimilarity : subject_information_content
      PairwiseSimilarity : subject_label
      PairwiseSimilarity : subject_source
      
```





## Inheritance
* **PairwiseSimilarity**
    * [TermPairwiseSimilarity](TermPairwiseSimilarity.md)
    * [TermSetPairwiseSimilarity](TermSetPairwiseSimilarity.md)



## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [subject_id](subject_id.md) | 1..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)  | The first of the two entities being compared  |
| [subject_label](subject_label.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  | the label or name for the first entity  |
| [subject_source](subject_source.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  | the source for the first entity  |
| [object_id](object_id.md) | 0..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)  | The second of the two entities being compared  |
| [object_label](object_label.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  | the label or name for the second entity  |
| [object_source](object_source.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  | the source for the second entity  |
| [ancestor_id](ancestor_id.md) | 0..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)  | the most recent common ancestor of the two compared entities  |
| [ancestor_label](ancestor_label.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  | the name or label of the ancestor concept  |
| [ancestor_source](ancestor_source.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [object_information_content](object_information_content.md) | 0..1 <br/> [NegativeLogValue](NegativeLogValue.md)  | The IC of the object  |
| [subject_information_content](subject_information_content.md) | 0..1 <br/> [NegativeLogValue](NegativeLogValue.md)  | The IC of the subject  |
| [ancestor_information_content](ancestor_information_content.md) | 0..1 <br/> [NegativeLogValue](NegativeLogValue.md)  | The IC of the object  |
| [jaccard_similarity](jaccard_similarity.md) | 0..1 <br/> [ZeroToOne](ZeroToOne.md)  | The number of concepts in the intersection divided by the number in the union  |
| [dice_similarity](dice_similarity.md) | 0..1 <br/> [ZeroToOne](ZeroToOne.md)  |   |
| [phenodigm_score](phenodigm_score.md) | 0..1 <br/> [NonNegativeFloat](NonNegativeFloat.md)  | the geometric mean of the jaccard similarity and the information content  |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/similarity







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['sim:PairwiseSimilarity'] |
| native | ['sim:PairwiseSimilarity'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PairwiseSimilarity
description: Abstract grouping for representing individual pairwise similarities
from_schema: https://w3id.org/linkml/similarity
rank: 1000
abstract: true
slots:
- subject_id
- subject_label
- subject_source
- object_id
- object_label
- object_source
- ancestor_id
- ancestor_label
- ancestor_source
- object_information_content
- subject_information_content
- ancestor_information_content
- jaccard_similarity
- dice_similarity
- phenodigm_score

```
</details>

### Induced

<details>
```yaml
name: PairwiseSimilarity
description: Abstract grouping for representing individual pairwise similarities
from_schema: https://w3id.org/linkml/similarity
rank: 1000
abstract: true
attributes:
  subject_id:
    name: subject_id
    description: The first of the two entities being compared
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    slot_uri: sssom:subject_id
    alias: subject_id
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: uriorcurie
    required: true
  subject_label:
    name: subject_label
    description: the label or name for the first entity
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    slot_uri: sssom:subject_label
    alias: subject_label
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: string
  subject_source:
    name: subject_source
    description: the source for the first entity
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    slot_uri: sssom:subject_source
    alias: subject_source
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: string
  object_id:
    name: object_id
    description: The second of the two entities being compared
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    slot_uri: sssom:object_id
    alias: object_id
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: uriorcurie
  object_label:
    name: object_label
    description: the label or name for the second entity
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    slot_uri: sssom:object_label
    alias: object_label
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: string
  object_source:
    name: object_source
    description: the source for the second entity
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    slot_uri: sssom:object_source
    alias: object_source
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: string
  ancestor_id:
    name: ancestor_id
    description: the most recent common ancestor of the two compared entities. If
      there are multiple MRCAs then the most informative one is selected
    todos:
    - decide on what to do when there are multiple possible ancestos
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    alias: ancestor_id
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: uriorcurie
  ancestor_label:
    name: ancestor_label
    description: the name or label of the ancestor concept
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    alias: ancestor_label
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: string
  ancestor_source:
    name: ancestor_source
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    alias: ancestor_source
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: string
  object_information_content:
    name: object_information_content
    description: The IC of the object
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    is_a: information_content
    alias: object_information_content
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: NegativeLogValue
  subject_information_content:
    name: subject_information_content
    description: The IC of the subject
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    is_a: information_content
    alias: subject_information_content
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: NegativeLogValue
  ancestor_information_content:
    name: ancestor_information_content
    description: The IC of the object
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    is_a: information_content
    alias: ancestor_information_content
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: NegativeLogValue
  jaccard_similarity:
    name: jaccard_similarity
    description: The number of concepts in the intersection divided by the number
      in the union
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    is_a: score
    alias: jaccard_similarity
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: ZeroToOne
  dice_similarity:
    name: dice_similarity
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    is_a: score
    alias: dice_similarity
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: ZeroToOne
  phenodigm_score:
    name: phenodigm_score
    description: the geometric mean of the jaccard similarity and the information
      content
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    is_a: score
    alias: phenodigm_score
    owner: PairwiseSimilarity
    domain_of:
    - PairwiseSimilarity
    range: NonNegativeFloat
    equals_expression: sqrt({jaccard_similarity} * {information_content})

```
</details>