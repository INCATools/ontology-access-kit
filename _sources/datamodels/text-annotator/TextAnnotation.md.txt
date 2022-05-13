# Class: TextAnnotation
_An individual text annotation_





URI: [ann:TextAnnotation](https://w3id.org/linkml/text_annotator/TextAnnotation)




## Inheritance

* **TextAnnotation** [ HasSpan]




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [predicate_id](predicate_id.md) | [string](string.md) | 0..1 | None  | . |
| [object_id](object_id.md) | [string](string.md) | 0..1 | None  | . |
| [object_label](object_label.md) | [string](string.md) | 0..1 | None  | . |
| [object_source](object_source.md) | [string](string.md) | 0..1 | None  | . |
| [confidence](confidence.md) | [float](float.md) | 0..1 | None  | . |
| [match_string](match_string.md) | [string](string.md) | 0..1 | None  | . |
| [is_longest_match](is_longest_match.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [match_type](match_type.md) | [string](string.md) | 0..1 | None  | . |
| [info](info.md) | [string](string.md) | 0..1 | None  | . |
| [subject_start](subject_start.md) | [Position](Position.md) | 0..1 | None  | . |
| [subject_end](subject_end.md) | [Position](Position.md) | 0..1 | None  | . |
| [subject_label](subject_label.md) | [string](string.md) | 0..1 | The portion of the subject text that is matched, ranging from subject_start to subject_end  | . |
| [subject_source](subject_source.md) | [string](string.md) | 0..1 | None  | . |
| [subject_text_id](subject_text_id.md) | [TextualElement](TextualElement.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [TextAnnotationResultSet](TextAnnotationResultSet.md) | [annotations](annotations.md) | range | TextAnnotation |



## Identifier and Mapping Information









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
    exact_mappings:
    - bpa:annotatedClass.id
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:object_id
  object_label:
    name: object_label
    exact_mappings:
    - bpa:annotatedClass.prefLabel
    from_schema: https://w3id.org/linkml/text_annotator
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
  match_type:
    name: match_type
    from_schema: https://w3id.org/linkml/text_annotator
  info:
    name: info
    from_schema: https://w3id.org/linkml/text_annotator

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
    exact_mappings:
    - bpa:annotatedClass.id
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:object_id
    alias: object_id
    owner: TextAnnotation
    range: string
  object_label:
    name: object_label
    exact_mappings:
    - bpa:annotatedClass.prefLabel
    from_schema: https://w3id.org/linkml/text_annotator
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
    exact_mappings:
    - bpa:from
    from_schema: https://w3id.org/linkml/text_annotator
    alias: subject_start
    owner: TextAnnotation
    range: Position
  subject_end:
    name: subject_end
    exact_mappings:
    - bpa:to
    from_schema: https://w3id.org/linkml/text_annotator
    alias: subject_end
    owner: TextAnnotation
    range: Position
  subject_label:
    name: subject_label
    exact_mappings:
    - bpa:text
    description: The portion of the subject text that is matched, ranging from subject_start
      to subject_end
    from_schema: https://w3id.org/linkml/text_annotator
    alias: subject_label
    owner: TextAnnotation
    range: string
  subject_source:
    name: subject_source
    from_schema: https://w3id.org/linkml/text_annotator
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

```
</details>