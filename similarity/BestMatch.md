# Class: BestMatch




URI: [sim:BestMatch](https://w3id.org/linkml/similarity/BestMatch)




```{mermaid}
 classDiagram
    class BestMatch
      BestMatch : match_source
      BestMatch : match_source_label
      BestMatch : match_subsumer
      BestMatch : match_subsumer_label
      BestMatch : match_target
      BestMatch : match_target_label
      BestMatch : score
      BestMatch : similarity
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [match_source](match_source.md) | 1..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [match_source_label](match_source_label.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [match_target](match_target.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  | the entity matches  |
| [match_target_label](match_target_label.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [score](score.md) | 0..1 <br/> [xsd:float](http://www.w3.org/2001/XMLSchema#float)  |   |
| [match_subsumer](match_subsumer.md) | 0..1 <br/> [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI)  |   |
| [match_subsumer_label](match_subsumer_label.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [similarity](similarity.md) | 0..1 <br/> [TermPairwiseSimilarity](TermPairwiseSimilarity.md)  |   |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TermSetPairwiseSimilarity](TermSetPairwiseSimilarity.md) | [subject_best_matches](subject_best_matches.md) | range | BestMatch |
| [TermSetPairwiseSimilarity](TermSetPairwiseSimilarity.md) | [object_best_matches](object_best_matches.md) | range | BestMatch |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/similarity







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['sim:BestMatch'] |
| native | ['sim:BestMatch'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: BestMatch
from_schema: https://w3id.org/linkml/similarity
rank: 1000
attributes:
  match_source:
    name: match_source
    comments:
    - note that the match_source is either the subject or the object
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    identifier: true
  match_source_label:
    name: match_source_label
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
  match_target:
    name: match_target
    description: the entity matches
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
  match_target_label:
    name: match_target_label
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
  score:
    name: score
    from_schema: https://w3id.org/linkml/similarity
    range: float
  match_subsumer:
    name: match_subsumer
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    range: uriorcurie
  match_subsumer_label:
    name: match_subsumer_label
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
  similarity:
    name: similarity
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    range: TermPairwiseSimilarity

```
</details>

### Induced

<details>
```yaml
name: BestMatch
from_schema: https://w3id.org/linkml/similarity
rank: 1000
attributes:
  match_source:
    name: match_source
    comments:
    - note that the match_source is either the subject or the object
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    identifier: true
    alias: match_source
    owner: BestMatch
    domain_of:
    - BestMatch
    range: string
  match_source_label:
    name: match_source_label
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    alias: match_source_label
    owner: BestMatch
    domain_of:
    - BestMatch
    range: string
  match_target:
    name: match_target
    description: the entity matches
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    alias: match_target
    owner: BestMatch
    domain_of:
    - BestMatch
    range: string
  match_target_label:
    name: match_target_label
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    alias: match_target_label
    owner: BestMatch
    domain_of:
    - BestMatch
    range: string
  score:
    name: score
    from_schema: https://w3id.org/linkml/similarity
    alias: score
    owner: BestMatch
    domain_of:
    - BestMatch
    range: float
  match_subsumer:
    name: match_subsumer
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    alias: match_subsumer
    owner: BestMatch
    domain_of:
    - BestMatch
    range: uriorcurie
  match_subsumer_label:
    name: match_subsumer_label
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    alias: match_subsumer_label
    owner: BestMatch
    domain_of:
    - BestMatch
    range: string
  similarity:
    name: similarity
    from_schema: https://w3id.org/linkml/similarity
    rank: 1000
    alias: similarity
    owner: BestMatch
    domain_of:
    - BestMatch
    range: TermPairwiseSimilarity

```
</details>