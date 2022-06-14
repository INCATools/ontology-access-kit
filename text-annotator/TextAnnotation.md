# Class: TextAnnotation
_An individual text annotation_





URI: [oa:Annotation](http://www.w3.org/ns/oa#Annotation)




```{mermaid}
 classDiagram
      HasSpan <|-- TextAnnotation
      
      TextAnnotation : confidence
      TextAnnotation : info
      TextAnnotation : is_longest_match
      TextAnnotation : match_string
      TextAnnotation : match_type
      TextAnnotation : matches_whole_text
      TextAnnotation : object_id
      TextAnnotation : object_label
      TextAnnotation : object_source
      TextAnnotation : predicate_id
      TextAnnotation : subject_end
      TextAnnotation : subject_label
      TextAnnotation : subject_source
      TextAnnotation : subject_start
      TextAnnotation : subject_text_id
      

```





## Inheritance
* **TextAnnotation** [ HasSpan]



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [predicate_id](predicate_id.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [object_id](object_id.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [object_label](object_label.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [object_source](object_source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [confidence](confidence.md) | [xsd:float](http://www.w3.org/2001/XMLSchema#float) | 0..1 | None  | . |
| [match_string](match_string.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [is_longest_match](is_longest_match.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [matches_whole_text](matches_whole_text.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [match_type](match_type.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [info](info.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [subject_start](subject_start.md) | [Position](Position.md) | 0..1 | None  | . |
| [subject_end](subject_end.md) | [Position](Position.md) | 0..1 | None  | . |
| [subject_label](subject_label.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | The portion of the subject text that is matched, ranging from subject_start to subject_end  | . |
| [subject_source](subject_source.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [subject_text_id](subject_text_id.md) | [TextualElement](TextualElement.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TextAnnotationResultSet](TextAnnotationResultSet.md) | [annotations](annotations.md) | range | TextAnnotation |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/text_annotator







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['oa:Annotation'] |
| native | ['ann:TextAnnotation'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TextAnnotation
description: An individual text annotation
from_schema: https://w3id.org/linkml/text_annotator
mixins:
- HasSpan
attributes:
  predicate_id:
    name: predicate_id
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:predicate_id
  object_id:
    name: object_id
    from_schema: https://w3id.org/linkml/text_annotator
    exact_mappings:
    - bpa:annotatedClass.id
    slot_uri: sssom:object_id
  object_label:
    name: object_label
    from_schema: https://w3id.org/linkml/text_annotator
    exact_mappings:
    - bpa:annotatedClass.prefLabel
    slot_uri: sssom:object_label
  object_source:
    name: object_source
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:object_source
  confidence:
    name: confidence
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:confidence
    range: float
  match_string:
    name: match_string
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:match_string
  is_longest_match:
    name: is_longest_match
    from_schema: https://w3id.org/linkml/text_annotator
    range: boolean
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/linkml/text_annotator
    range: boolean
  match_type:
    name: match_type
    from_schema: https://w3id.org/linkml/text_annotator
  info:
    name: info
    from_schema: https://w3id.org/linkml/text_annotator
class_uri: oa:Annotation

```
</details>

### Induced

<details>
```yaml
name: TextAnnotation
description: An individual text annotation
from_schema: https://w3id.org/linkml/text_annotator
mixins:
- HasSpan
attributes:
  predicate_id:
    name: predicate_id
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:predicate_id
    alias: predicate_id
    owner: TextAnnotation
    range: string
  object_id:
    name: object_id
    from_schema: https://w3id.org/linkml/text_annotator
    exact_mappings:
    - bpa:annotatedClass.id
    slot_uri: sssom:object_id
    alias: object_id
    owner: TextAnnotation
    range: string
  object_label:
    name: object_label
    from_schema: https://w3id.org/linkml/text_annotator
    exact_mappings:
    - bpa:annotatedClass.prefLabel
    slot_uri: sssom:object_label
    alias: object_label
    owner: TextAnnotation
    range: string
  object_source:
    name: object_source
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:object_source
    alias: object_source
    owner: TextAnnotation
    range: string
  confidence:
    name: confidence
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:confidence
    alias: confidence
    owner: TextAnnotation
    range: float
  match_string:
    name: match_string
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:match_string
    alias: match_string
    owner: TextAnnotation
    range: string
  is_longest_match:
    name: is_longest_match
    from_schema: https://w3id.org/linkml/text_annotator
    alias: is_longest_match
    owner: TextAnnotation
    range: boolean
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/linkml/text_annotator
    alias: matches_whole_text
    owner: TextAnnotation
    range: boolean
  match_type:
    name: match_type
    from_schema: https://w3id.org/linkml/text_annotator
    alias: match_type
    owner: TextAnnotation
    range: string
  info:
    name: info
    from_schema: https://w3id.org/linkml/text_annotator
    alias: info
    owner: TextAnnotation
    range: string
  subject_start:
    name: subject_start
    from_schema: https://w3id.org/linkml/text_annotator
    exact_mappings:
    - bpa:from
    alias: subject_start
    owner: TextAnnotation
    range: Position
  subject_end:
    name: subject_end
    from_schema: https://w3id.org/linkml/text_annotator
    exact_mappings:
    - bpa:to
    alias: subject_end
    owner: TextAnnotation
    range: Position
  subject_label:
    name: subject_label
    description: The portion of the subject text that is matched, ranging from subject_start
      to subject_end
    from_schema: https://w3id.org/linkml/text_annotator
    exact_mappings:
    - bpa:text
    alias: subject_label
    owner: TextAnnotation
    range: string
  subject_source:
    name: subject_source
    from_schema: https://w3id.org/linkml/text_annotator
    exact_mappings:
    - oa:hasBody
    slot_uri: sssom:subject_source
    alias: subject_source
    owner: TextAnnotation
    range: string
  subject_text_id:
    name: subject_text_id
    from_schema: https://w3id.org/linkml/text_annotator
    alias: subject_text_id
    owner: TextAnnotation
    range: TextualElement
class_uri: oa:Annotation

```
</details>