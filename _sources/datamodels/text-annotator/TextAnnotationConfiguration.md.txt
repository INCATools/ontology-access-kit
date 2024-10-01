

# Class: TextAnnotationConfiguration


_configuration for search_





URI: [ann:TextAnnotationConfiguration](https://w3id.org/linkml/text_annotator/TextAnnotationConfiguration)






```{mermaid}
 classDiagram
    class TextAnnotationConfiguration
    click TextAnnotationConfiguration href "../TextAnnotationConfiguration"
      TextAnnotationConfiguration : categories
        
      TextAnnotationConfiguration : include_aliases
        
      TextAnnotationConfiguration : limit
        
      TextAnnotationConfiguration : matches_whole_text
        
      TextAnnotationConfiguration : model
        
      TextAnnotationConfiguration : sources
        
      TextAnnotationConfiguration : token_exclusion_list
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [matches_whole_text](matches_whole_text.md) | 0..1 <br/> [Boolean](Boolean.md) | If true, then only grounding is performed, and the entire text is used as the... | direct |
| [sources](sources.md) | * <br/> [String](String.md) |  | direct |
| [limit](limit.md) | 0..1 <br/> [Integer](Integer.md) | The maximum number of annotations to return | direct |
| [token_exclusion_list](token_exclusion_list.md) | * <br/> [String](String.md) | A list of tokens to exclude from the annotation process | direct |
| [categories](categories.md) | * <br/> [String](String.md) | A list of named entity categories to include | direct |
| [model](model.md) | 0..1 <br/> [String](String.md) | The name of the model to use for annotation | direct |
| [include_aliases](include_aliases.md) | 0..1 <br/> [Boolean](Boolean.md) | If true, then the aliases (synonyms) of the matched entity are included in th... | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:TextAnnotationConfiguration |
| native | ann:TextAnnotationConfiguration |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TextAnnotationConfiguration
description: configuration for search
from_schema: https://w3id.org/oak/text_annotator
attributes:
  matches_whole_text:
    name: matches_whole_text
    description: If true, then only grounding is performed, and the entire text is
      used as the match string.
    from_schema: https://w3id.org/oak/text_annotator
    aliases:
    - grounding_mode
    rank: 1000
    domain_of:
    - TextAnnotationConfiguration
    - TextAnnotation
    range: boolean
  sources:
    name: sources
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotationConfiguration
    multivalued: true
  limit:
    name: limit
    description: The maximum number of annotations to return
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotationConfiguration
    range: integer
  token_exclusion_list:
    name: token_exclusion_list
    description: A list of tokens to exclude from the annotation process
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotationConfiguration
    multivalued: true
  categories:
    name: categories
    description: A list of named entity categories to include.
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotationConfiguration
    multivalued: true
  model:
    name: model
    description: The name of the model to use for annotation. The specifics of this
      are implementation-dependent.
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotationConfiguration
    range: string
  include_aliases:
    name: include_aliases
    description: If true, then the aliases (synonyms) of the matched entity are included
      in the annotation results.
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotationConfiguration
    range: boolean

```
</details>

### Induced

<details>
```yaml
name: TextAnnotationConfiguration
description: configuration for search
from_schema: https://w3id.org/oak/text_annotator
attributes:
  matches_whole_text:
    name: matches_whole_text
    description: If true, then only grounding is performed, and the entire text is
      used as the match string.
    from_schema: https://w3id.org/oak/text_annotator
    aliases:
    - grounding_mode
    rank: 1000
    alias: matches_whole_text
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    - TextAnnotation
    range: boolean
  sources:
    name: sources
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: sources
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: string
    multivalued: true
  limit:
    name: limit
    description: The maximum number of annotations to return
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: limit
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: integer
  token_exclusion_list:
    name: token_exclusion_list
    description: A list of tokens to exclude from the annotation process
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: token_exclusion_list
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: string
    multivalued: true
  categories:
    name: categories
    description: A list of named entity categories to include.
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: categories
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: string
    multivalued: true
  model:
    name: model
    description: The name of the model to use for annotation. The specifics of this
      are implementation-dependent.
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: model
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: string
  include_aliases:
    name: include_aliases
    description: If true, then the aliases (synonyms) of the matched entity are included
      in the annotation results.
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: include_aliases
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: boolean

```
</details>