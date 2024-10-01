

# Class: TermPairwiseSimilarity


_A simple pairwise similarity between two atomic concepts/terms_





URI: [sim:TermPairwiseSimilarity](https://w3id.org/linkml/similarity/TermPairwiseSimilarity)






```{mermaid}
 classDiagram
    class TermPairwiseSimilarity
    click TermPairwiseSimilarity href "../TermPairwiseSimilarity"
      PairwiseSimilarity <|-- TermPairwiseSimilarity
        click PairwiseSimilarity href "../PairwiseSimilarity"
      
      TermPairwiseSimilarity : ancestor_id
        
      TermPairwiseSimilarity : ancestor_information_content
        
      TermPairwiseSimilarity : ancestor_label
        
      TermPairwiseSimilarity : ancestor_source
        
      TermPairwiseSimilarity : cosine_similarity
        
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

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject_id](subject_id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | The first of the two entities being compared | direct |
| [subject_label](subject_label.md) | 0..1 <br/> [String](String.md) | the label or name for the first entity | direct |
| [subject_source](subject_source.md) | 0..1 <br/> [String](String.md) | the source for the first entity | direct |
| [object_id](object_id.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | The second of the two entities being compared | direct |
| [object_label](object_label.md) | 0..1 <br/> [String](String.md) | the label or name for the second entity | direct |
| [object_source](object_source.md) | 0..1 <br/> [String](String.md) | the source for the second entity | direct |
| [ancestor_id](ancestor_id.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) | the most recent common ancestor of the two compared entities | direct |
| [ancestor_label](ancestor_label.md) | 0..1 <br/> [String](String.md) | the name or label of the ancestor concept | direct |
| [ancestor_source](ancestor_source.md) | 0..1 <br/> [String](String.md) |  | direct |
| [object_information_content](object_information_content.md) | 0..1 <br/> [NegativeLogValue](NegativeLogValue.md) | The IC of the object | direct |
| [subject_information_content](subject_information_content.md) | 0..1 <br/> [NegativeLogValue](NegativeLogValue.md) | The IC of the subject | direct |
| [ancestor_information_content](ancestor_information_content.md) | 0..1 <br/> [NegativeLogValue](NegativeLogValue.md) | The IC of the object | direct |
| [jaccard_similarity](jaccard_similarity.md) | 0..1 <br/> [ZeroToOne](ZeroToOne.md) | The number of concepts in the intersection divided by the number in the union | direct |
| [cosine_similarity](cosine_similarity.md) | 0..1 <br/> [Float](Float.md) | the dot product of two node embeddings divided by the product of their length... | direct |
| [dice_similarity](dice_similarity.md) | 0..1 <br/> [ZeroToOne](ZeroToOne.md) |  | direct |
| [phenodigm_score](phenodigm_score.md) | 0..1 <br/> [NonNegativeFloat](NonNegativeFloat.md) | the geometric mean of the jaccard similarity and the information content | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [BestMatch](BestMatch.md) | [similarity](similarity.md) | range | [TermPairwiseSimilarity](TermPairwiseSimilarity.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:TermPairwiseSimilarity |
| native | sim:TermPairwiseSimilarity |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TermPairwiseSimilarity
description: A simple pairwise similarity between two atomic concepts/terms
from_schema: https://w3id.org/oak/similarity
is_a: PairwiseSimilarity
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
- cosine_similarity
- dice_similarity
- phenodigm_score

```
</details>

### Induced

<details>
```yaml
name: TermPairwiseSimilarity
description: A simple pairwise similarity between two atomic concepts/terms
from_schema: https://w3id.org/oak/similarity
is_a: PairwiseSimilarity
attributes:
  subject_id:
    name: subject_id
    description: The first of the two entities being compared
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    slot_uri: sssom:subject_id
    alias: subject_id
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: uriorcurie
    required: true
  subject_label:
    name: subject_label
    description: the label or name for the first entity
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    slot_uri: sssom:subject_label
    alias: subject_label
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: string
  subject_source:
    name: subject_source
    description: the source for the first entity
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    slot_uri: sssom:subject_source
    alias: subject_source
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: string
  object_id:
    name: object_id
    description: The second of the two entities being compared
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    slot_uri: sssom:object_id
    alias: object_id
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: uriorcurie
  object_label:
    name: object_label
    description: the label or name for the second entity
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    slot_uri: sssom:object_label
    alias: object_label
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: string
  object_source:
    name: object_source
    description: the source for the second entity
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    slot_uri: sssom:object_source
    alias: object_source
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: string
  ancestor_id:
    name: ancestor_id
    description: the most recent common ancestor of the two compared entities. If
      there are multiple MRCAs then the most informative one is selected
    todos:
    - decide on what to do when there are multiple possible ancestos
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: ancestor_id
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: uriorcurie
  ancestor_label:
    name: ancestor_label
    description: the name or label of the ancestor concept
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: ancestor_label
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: string
  ancestor_source:
    name: ancestor_source
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: ancestor_source
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: string
  object_information_content:
    name: object_information_content
    description: The IC of the object
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    is_a: information_content
    alias: object_information_content
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: NegativeLogValue
  subject_information_content:
    name: subject_information_content
    description: The IC of the subject
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    is_a: information_content
    alias: subject_information_content
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: NegativeLogValue
  ancestor_information_content:
    name: ancestor_information_content
    description: The IC of the object
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    is_a: information_content
    alias: ancestor_information_content
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: NegativeLogValue
  jaccard_similarity:
    name: jaccard_similarity
    description: The number of concepts in the intersection divided by the number
      in the union
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    is_a: score
    alias: jaccard_similarity
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: ZeroToOne
  cosine_similarity:
    name: cosine_similarity
    description: the dot product of two node embeddings divided by the product of
      their lengths
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    is_a: score
    alias: cosine_similarity
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: float
  dice_similarity:
    name: dice_similarity
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    is_a: score
    alias: dice_similarity
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: ZeroToOne
  phenodigm_score:
    name: phenodigm_score
    description: the geometric mean of the jaccard similarity and the information
      content
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    is_a: score
    alias: phenodigm_score
    owner: TermPairwiseSimilarity
    domain_of:
    - TermPairwiseSimilarity
    range: NonNegativeFloat
    equals_expression: sqrt({jaccard_similarity} * {information_content})

```
</details>