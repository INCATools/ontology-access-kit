# Class: TermSetPairwiseSimilarity
_A simple pairwise similarity between two sets of concepts/terms_




URI: [sim:TermSetPairwiseSimilarity](https://w3id.org/linkml/similarity/TermSetPairwiseSimilarity)



```{mermaid}
 classDiagram
    class TermSetPairwiseSimilarity
      PairwiseSimilarity <|-- TermSetPairwiseSimilarity
      
      TermSetPairwiseSimilarity : average_score
        
      TermSetPairwiseSimilarity : best_score
        
      TermSetPairwiseSimilarity : metric
        
      TermSetPairwiseSimilarity : object_best_matches
        
          TermSetPairwiseSimilarity ..> BestMatch : object_best_matches
        
      TermSetPairwiseSimilarity : object_termset
        
          TermSetPairwiseSimilarity ..> TermInfo : object_termset
        
      TermSetPairwiseSimilarity : subject_best_matches
        
          TermSetPairwiseSimilarity ..> BestMatch : subject_best_matches
        
      TermSetPairwiseSimilarity : subject_termset
        
          TermSetPairwiseSimilarity ..> TermInfo : subject_termset
        
      
```





## Inheritance
* [PairwiseSimilarity](PairwiseSimilarity.md)
    * **TermSetPairwiseSimilarity**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject_termset](subject_termset.md) | 0..* <br/> [TermInfo](TermInfo.md) |  | direct |
| [object_termset](object_termset.md) | 0..* <br/> [TermInfo](TermInfo.md) |  | direct |
| [subject_best_matches](subject_best_matches.md) | 0..* <br/> [BestMatch](BestMatch.md) |  | direct |
| [object_best_matches](object_best_matches.md) | 0..* <br/> [BestMatch](BestMatch.md) |  | direct |
| [average_score](average_score.md) | 0..1 <br/> [Float](Float.md) |  | direct |
| [best_score](best_score.md) | 0..1 <br/> [Float](Float.md) |  | direct |
| [metric](metric.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:TermSetPairwiseSimilarity |
| native | sim:TermSetPairwiseSimilarity |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TermSetPairwiseSimilarity
description: A simple pairwise similarity between two sets of concepts/terms
from_schema: https://w3id.org/oak/similarity
rank: 1000
is_a: PairwiseSimilarity
slots:
- subject_termset
- object_termset
- subject_best_matches
- object_best_matches
- average_score
- best_score
- metric

```
</details>

### Induced

<details>
```yaml
name: TermSetPairwiseSimilarity
description: A simple pairwise similarity between two sets of concepts/terms
from_schema: https://w3id.org/oak/similarity
rank: 1000
is_a: PairwiseSimilarity
attributes:
  subject_termset:
    name: subject_termset
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    multivalued: true
    alias: subject_termset
    owner: TermSetPairwiseSimilarity
    domain_of:
    - TermSetPairwiseSimilarity
    range: TermInfo
    inlined: true
  object_termset:
    name: object_termset
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    multivalued: true
    alias: object_termset
    owner: TermSetPairwiseSimilarity
    domain_of:
    - TermSetPairwiseSimilarity
    range: TermInfo
    inlined: true
  subject_best_matches:
    name: subject_best_matches
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    multivalued: true
    alias: subject_best_matches
    owner: TermSetPairwiseSimilarity
    domain_of:
    - TermSetPairwiseSimilarity
    range: BestMatch
    inlined: true
  object_best_matches:
    name: object_best_matches
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    multivalued: true
    alias: object_best_matches
    owner: TermSetPairwiseSimilarity
    domain_of:
    - TermSetPairwiseSimilarity
    range: BestMatch
    inlined: true
  average_score:
    name: average_score
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: average_score
    owner: TermSetPairwiseSimilarity
    domain_of:
    - TermSetPairwiseSimilarity
    range: float
    required: false
  best_score:
    name: best_score
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: best_score
    owner: TermSetPairwiseSimilarity
    domain_of:
    - TermSetPairwiseSimilarity
    range: float
    required: false
  metric:
    name: metric
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: metric
    owner: TermSetPairwiseSimilarity
    domain_of:
    - TermSetPairwiseSimilarity
    range: uriorcurie

```
</details>