

# Class: InformationContentMethod


_Describes how information content (IC) scores were computed. IC scores are only comparable if they were computed using the same method. If absent, IC scores are assumed to be log2 bits computed by OAK using the ontology as the corpus._





URI: [sim:InformationContentMethod](https://w3id.org/linkml/similarity/InformationContentMethod)






```{mermaid}
 classDiagram
    class InformationContentMethod
    click InformationContentMethod href "../InformationContentMethod"
      InformationContentMethod : background_count
        
      InformationContentMethod : closure_predicates
        
      InformationContentMethod : corpus
        
          
    
    
    InformationContentMethod --> "0..1" InformationContentCorpusEnum : corpus
    click InformationContentCorpusEnum href "../InformationContentCorpusEnum"

        
      InformationContentMethod : scale
        
          
    
    
    InformationContentMethod --> "1" InformationContentScaleEnum : scale
    click InformationContentScaleEnum href "../InformationContentScaleEnum"

        
      InformationContentMethod : source
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [scale](scale.md) | 1 <br/> [InformationContentScaleEnum](InformationContentScaleEnum.md) | The scale or units of the IC scores | direct |
| [corpus](corpus.md) | 0..1 <br/> [InformationContentCorpusEnum](InformationContentCorpusEnum.md) | The corpus used to determine term frequencies | direct |
| [closure_predicates](closure_predicates.md) | * <br/> [Uriorcurie](Uriorcurie.md) | The predicates used to compute the reflexive transitive closure when determin... | direct |
| [background_count](background_count.md) | 0..1 <br/> [ItemCount](ItemCount.md) | The number of items (terms or annotated entities) in the background set, i | direct |
| [source](source.md) | 0..1 <br/> [String](String.md) | The system or resource that computed the scores, e | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TermPairwiseSimilarity](TermPairwiseSimilarity.md) | [information_content_method](information_content_method.md) | range | [InformationContentMethod](InformationContentMethod.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/similarity




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sim:InformationContentMethod |
| native | sim:InformationContentMethod |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: InformationContentMethod
description: Describes how information content (IC) scores were computed. IC scores
  are only comparable if they were computed using the same method. If absent, IC scores
  are assumed to be log2 bits computed by OAK using the ontology as the corpus.
from_schema: https://w3id.org/oak/similarity
attributes:
  scale:
    name: scale
    description: The scale or units of the IC scores
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    domain_of:
    - InformationContentMethod
    range: InformationContentScaleEnum
    required: true
  corpus:
    name: corpus
    description: The corpus used to determine term frequencies
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    domain_of:
    - InformationContentMethod
    range: InformationContentCorpusEnum
  closure_predicates:
    name: closure_predicates
    description: The predicates used to compute the reflexive transitive closure when
      determining term frequencies. If empty, all predicates are used.
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    domain_of:
    - InformationContentMethod
    range: uriorcurie
    multivalued: true
  background_count:
    name: background_count
    description: The number of items (terms or annotated entities) in the background
      set, i.e. N in Pr(t) = freq(t)/N
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    domain_of:
    - InformationContentMethod
    range: ItemCount
  source:
    name: source
    description: The system or resource that computed the scores, e.g. oaklib, ubergraph
    examples:
    - value: ubergraph
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    domain_of:
    - InformationContentMethod

```
</details>

### Induced

<details>
```yaml
name: InformationContentMethod
description: Describes how information content (IC) scores were computed. IC scores
  are only comparable if they were computed using the same method. If absent, IC scores
  are assumed to be log2 bits computed by OAK using the ontology as the corpus.
from_schema: https://w3id.org/oak/similarity
attributes:
  scale:
    name: scale
    description: The scale or units of the IC scores
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: scale
    owner: InformationContentMethod
    domain_of:
    - InformationContentMethod
    range: InformationContentScaleEnum
    required: true
  corpus:
    name: corpus
    description: The corpus used to determine term frequencies
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: corpus
    owner: InformationContentMethod
    domain_of:
    - InformationContentMethod
    range: InformationContentCorpusEnum
  closure_predicates:
    name: closure_predicates
    description: The predicates used to compute the reflexive transitive closure when
      determining term frequencies. If empty, all predicates are used.
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: closure_predicates
    owner: InformationContentMethod
    domain_of:
    - InformationContentMethod
    range: uriorcurie
    multivalued: true
  background_count:
    name: background_count
    description: The number of items (terms or annotated entities) in the background
      set, i.e. N in Pr(t) = freq(t)/N
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: background_count
    owner: InformationContentMethod
    domain_of:
    - InformationContentMethod
    range: ItemCount
  source:
    name: source
    description: The system or resource that computed the scores, e.g. oaklib, ubergraph
    examples:
    - value: ubergraph
    from_schema: https://w3id.org/oak/similarity
    rank: 1000
    alias: source
    owner: InformationContentMethod
    domain_of:
    - InformationContentMethod
    range: string

```
</details>