# Class: TextAnnotationConfiguration
_configuration for search_




URI: [ann:TextAnnotationConfiguration](https://w3id.org/linkml/text_annotator/TextAnnotationConfiguration)



```{mermaid}
 classDiagram
    class TextAnnotationConfiguration
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
| [matches_whole_text](matches_whole_text.md) | 0..1 <br/> [String](String.md) |  | direct |
| [sources](sources.md) | 0..* <br/> [String](String.md) |  | direct |
| [limit](limit.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |
| [token_exclusion_list](token_exclusion_list.md) | 0..* <br/> [String](String.md) |  | direct |
| [model](model.md) | 0..1 <br/> [String](String.md) |  | direct |
| [include_aliases](include_aliases.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |









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
rank: 1000
attributes:
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    range: boolean
  sources:
    name: sources
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    multivalued: true
  limit:
    name: limit
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    range: integer
  token_exclusion_list:
    name: token_exclusion_list
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    multivalued: true
  model:
    name: model
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    range: string
  include_aliases:
    name: include_aliases
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    range: boolean

```
</details>

### Induced

<details>
```yaml
name: TextAnnotationConfiguration
description: configuration for search
from_schema: https://w3id.org/oak/text_annotator
rank: 1000
attributes:
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/oak/text_annotator
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
    multivalued: true
    alias: sources
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: string
  limit:
    name: limit
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: limit
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: integer
  token_exclusion_list:
    name: token_exclusion_list
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    multivalued: true
    alias: token_exclusion_list
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: string
  model:
    name: model
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: model
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: string
  include_aliases:
    name: include_aliases
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: include_aliases
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: boolean

```
</details>