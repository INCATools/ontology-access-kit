

# Class: TextAnnotation


_An individual text annotation_





URI: [oa:Annotation](http://www.w3.org/ns/oa#Annotation)






```{mermaid}
 classDiagram
    class TextAnnotation
    click TextAnnotation href "../TextAnnotation"
      HasSpan <|-- TextAnnotation
        click HasSpan href "../HasSpan"
      
      TextAnnotation : confidence
        
      TextAnnotation : info
        
      TextAnnotation : is_longest_match
        
      TextAnnotation : match_string
        
      TextAnnotation : match_type
        
      TextAnnotation : matches_whole_text
        
      TextAnnotation : object_aliases
        
      TextAnnotation : object_categories
        
      TextAnnotation : object_id
        
      TextAnnotation : object_label
        
      TextAnnotation : object_source
        
      TextAnnotation : predicate_id
        
      TextAnnotation : subject_end
        
      TextAnnotation : subject_label
        
      TextAnnotation : subject_source
        
      TextAnnotation : subject_start
        
      TextAnnotation : subject_text_id
        
          
    
    
    TextAnnotation --> "0..1" TextualElement : subject_text_id
    click TextualElement href "../TextualElement"

        
      
```





## Inheritance
* **TextAnnotation** [ [HasSpan](HasSpan.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [predicate_id](predicate_id.md) | 0..1 <br/> [String](String.md) |  | direct |
| [object_id](object_id.md) | 0..1 <br/> [String](String.md) |  | direct |
| [object_label](object_label.md) | 0..1 <br/> [String](String.md) |  | direct |
| [object_categories](object_categories.md) | * <br/> [String](String.md) |  | direct |
| [object_source](object_source.md) | 0..1 <br/> [String](String.md) |  | direct |
| [confidence](confidence.md) | 0..1 <br/> [Float](Float.md) |  | direct |
| [match_string](match_string.md) | 0..1 <br/> [String](String.md) |  | direct |
| [is_longest_match](is_longest_match.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [matches_whole_text](matches_whole_text.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [match_type](match_type.md) | 0..1 <br/> [String](String.md) |  | direct |
| [info](info.md) | 0..1 <br/> [String](String.md) |  | direct |
| [object_aliases](object_aliases.md) | * <br/> [String](String.md) |  | direct |
| [subject_start](subject_start.md) | 0..1 <br/> [Position](Position.md) |  | [HasSpan](HasSpan.md) |
| [subject_end](subject_end.md) | 0..1 <br/> [Position](Position.md) |  | [HasSpan](HasSpan.md) |
| [subject_label](subject_label.md) | 0..1 <br/> [String](String.md) | The portion of the subject text that is matched, ranging from subject_start t... | [HasSpan](HasSpan.md) |
| [subject_source](subject_source.md) | 0..1 <br/> [String](String.md) |  | [HasSpan](HasSpan.md) |
| [subject_text_id](subject_text_id.md) | 0..1 <br/> [TextualElement](TextualElement.md) |  | [HasSpan](HasSpan.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TextAnnotationResultSet](TextAnnotationResultSet.md) | [annotations](annotations.md) | range | [TextAnnotation](TextAnnotation.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oa:Annotation |
| native | ann:TextAnnotation |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TextAnnotation
description: An individual text annotation
from_schema: https://w3id.org/oak/text_annotator
mixins:
- HasSpan
attributes:
  predicate_id:
    name: predicate_id
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    slot_uri: sssom:predicate_id
    domain_of:
    - TextAnnotation
  object_id:
    name: object_id
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:annotatedClass.id
    rank: 1000
    slot_uri: sssom:object_id
    domain_of:
    - TextAnnotation
  object_label:
    name: object_label
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:annotatedClass.prefLabel
    rank: 1000
    slot_uri: sssom:object_label
    domain_of:
    - TextAnnotation
  object_categories:
    name: object_categories
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotation
    multivalued: true
  object_source:
    name: object_source
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    slot_uri: sssom:object_source
    domain_of:
    - TextAnnotation
  confidence:
    name: confidence
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    slot_uri: sssom:confidence
    domain_of:
    - TextAnnotation
    range: float
  match_string:
    name: match_string
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    slot_uri: sssom:match_string
    domain_of:
    - TextAnnotation
  is_longest_match:
    name: is_longest_match
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotation
    range: boolean
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/oak/text_annotator
    domain_of:
    - TextAnnotationConfiguration
    - TextAnnotation
    range: boolean
  match_type:
    name: match_type
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotation
  info:
    name: info
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotation
  object_aliases:
    name: object_aliases
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextAnnotation
    multivalued: true
class_uri: oa:Annotation

```
</details>

### Induced

<details>
```yaml
name: TextAnnotation
description: An individual text annotation
from_schema: https://w3id.org/oak/text_annotator
mixins:
- HasSpan
attributes:
  predicate_id:
    name: predicate_id
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    slot_uri: sssom:predicate_id
    alias: predicate_id
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: string
  object_id:
    name: object_id
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:annotatedClass.id
    rank: 1000
    slot_uri: sssom:object_id
    alias: object_id
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: string
  object_label:
    name: object_label
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:annotatedClass.prefLabel
    rank: 1000
    slot_uri: sssom:object_label
    alias: object_label
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: string
  object_categories:
    name: object_categories
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: object_categories
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: string
    multivalued: true
  object_source:
    name: object_source
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    slot_uri: sssom:object_source
    alias: object_source
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: string
  confidence:
    name: confidence
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    slot_uri: sssom:confidence
    alias: confidence
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: float
  match_string:
    name: match_string
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    slot_uri: sssom:match_string
    alias: match_string
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: string
  is_longest_match:
    name: is_longest_match
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: is_longest_match
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: boolean
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/oak/text_annotator
    alias: matches_whole_text
    owner: TextAnnotation
    domain_of:
    - TextAnnotationConfiguration
    - TextAnnotation
    range: boolean
  match_type:
    name: match_type
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: match_type
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: string
  info:
    name: info
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: info
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: string
  object_aliases:
    name: object_aliases
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: object_aliases
    owner: TextAnnotation
    domain_of:
    - TextAnnotation
    range: string
    multivalued: true
  subject_start:
    name: subject_start
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:from
    rank: 1000
    alias: subject_start
    owner: TextAnnotation
    domain_of:
    - HasSpan
    range: Position
  subject_end:
    name: subject_end
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:to
    rank: 1000
    alias: subject_end
    owner: TextAnnotation
    domain_of:
    - HasSpan
    range: Position
  subject_label:
    name: subject_label
    description: The portion of the subject text that is matched, ranging from subject_start
      to subject_end
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:text
    rank: 1000
    alias: subject_label
    owner: TextAnnotation
    domain_of:
    - HasSpan
    range: string
  subject_source:
    name: subject_source
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - oa:hasBody
    rank: 1000
    slot_uri: sssom:subject_source
    alias: subject_source
    owner: TextAnnotation
    domain_of:
    - HasSpan
    range: string
  subject_text_id:
    name: subject_text_id
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: subject_text_id
    owner: TextAnnotation
    domain_of:
    - HasSpan
    range: TextualElement
class_uri: oa:Annotation

```
</details>