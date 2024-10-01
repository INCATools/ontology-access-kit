

# Class: RelationshipToTerm


_A relationship of an ontology element to a lexical term_





URI: [mappingrules:RelationshipToTerm](https://w3id.org/oak/mapping-rules-datamodel/RelationshipToTerm)






```{mermaid}
 classDiagram
    class RelationshipToTerm
    click RelationshipToTerm href "../RelationshipToTerm"
      RelationshipToTerm : element
        
      RelationshipToTerm : element_term
        
      RelationshipToTerm : pipeline
        
          
    
    
    RelationshipToTerm --> "*" LexicalTransformationPipeline : pipeline
    click LexicalTransformationPipeline href "../LexicalTransformationPipeline"

        
      RelationshipToTerm : predicate
        
      RelationshipToTerm : source
        
      RelationshipToTerm : synonymized
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [predicate](predicate.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [element](element.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [element_term](element_term.md) | 0..1 <br/> [String](String.md) | the original term used in the element | direct |
| [source](source.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [pipeline](pipeline.md) | * <br/> [LexicalTransformationPipeline](LexicalTransformationPipeline.md) |  | direct |
| [synonymized](synonymized.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalGrouping](LexicalGrouping.md) | [relationships](relationships.md) | range | [RelationshipToTerm](RelationshipToTerm.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:RelationshipToTerm |
| native | mappingrules:RelationshipToTerm |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RelationshipToTerm
description: A relationship of an ontology element to a lexical term
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  predicate:
    name: predicate
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - RelationshipToTerm
    range: uriorcurie
  element:
    name: element
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - RelationshipToTerm
    range: uriorcurie
  element_term:
    name: element_term
    description: the original term used in the element
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - RelationshipToTerm
  source:
    name: source
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - RelationshipToTerm
    range: uriorcurie
  pipeline:
    name: pipeline
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - RelationshipToTerm
    range: LexicalTransformationPipeline
    multivalued: true
  synonymized:
    name: synonymized
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - RelationshipToTerm
    range: boolean

```
</details>

### Induced

<details>
```yaml
name: RelationshipToTerm
description: A relationship of an ontology element to a lexical term
from_schema: https://w3id.org/oak/mapping-rules-datamodel
attributes:
  predicate:
    name: predicate
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: predicate
    owner: RelationshipToTerm
    domain_of:
    - RelationshipToTerm
    range: uriorcurie
  element:
    name: element
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: element
    owner: RelationshipToTerm
    domain_of:
    - RelationshipToTerm
    range: uriorcurie
  element_term:
    name: element_term
    description: the original term used in the element
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: element_term
    owner: RelationshipToTerm
    domain_of:
    - RelationshipToTerm
    range: string
  source:
    name: source
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: source
    owner: RelationshipToTerm
    domain_of:
    - RelationshipToTerm
    range: uriorcurie
  pipeline:
    name: pipeline
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: pipeline
    owner: RelationshipToTerm
    domain_of:
    - RelationshipToTerm
    range: LexicalTransformationPipeline
    multivalued: true
  synonymized:
    name: synonymized
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: synonymized
    owner: RelationshipToTerm
    domain_of:
    - RelationshipToTerm
    range: boolean

```
</details>