# Class: HasSpan



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [ann:HasSpan](https://w3id.org/linkml/text_annotator/HasSpan)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [subject_start](subject_start.md) | [Position](Position.md) | 0..1 | None  | . |
| [subject_end](subject_end.md) | [Position](Position.md) | 0..1 | None  | . |
| [subject_label](subject_label.md) | [string](string.md) | 0..1 | The portion of the subject text that is matched, ranging from subject_start to subject_end  | . |
| [subject_source](subject_source.md) | [string](string.md) | 0..1 | None  | . |
| [subject_text_id](subject_text_id.md) | [TextualElement](TextualElement.md) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasSpan
from_schema: https://w3id.org/linkml/text_annotator
mixin: true
attributes:
  subject_start:
    name: subject_start
    exact_mappings:
    - bpa:from
    from_schema: https://w3id.org/linkml/text_annotator
    range: Position
  subject_end:
    name: subject_end
    exact_mappings:
    - bpa:to
    from_schema: https://w3id.org/linkml/text_annotator
    range: Position
  subject_label:
    name: subject_label
    exact_mappings:
    - bpa:text
    description: The portion of the subject text that is matched, ranging from subject_start
      to subject_end
    from_schema: https://w3id.org/linkml/text_annotator
  subject_source:
    name: subject_source
    exact_mappings:
    - oa:hasBody
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:subject_source
  subject_text_id:
    name: subject_text_id
    from_schema: https://w3id.org/linkml/text_annotator
    range: TextualElement

```
</details>

### Induced

<details>
```yaml
name: HasSpan
from_schema: https://w3id.org/linkml/text_annotator
mixin: true
attributes:
  subject_start:
    name: subject_start
    exact_mappings:
    - bpa:from
    from_schema: https://w3id.org/linkml/text_annotator
    alias: subject_start
    owner: HasSpan
    range: Position
  subject_end:
    name: subject_end
    exact_mappings:
    - bpa:to
    from_schema: https://w3id.org/linkml/text_annotator
    alias: subject_end
    owner: HasSpan
    range: Position
  subject_label:
    name: subject_label
    exact_mappings:
    - bpa:text
    description: The portion of the subject text that is matched, ranging from subject_start
      to subject_end
    from_schema: https://w3id.org/linkml/text_annotator
    alias: subject_label
    owner: HasSpan
    range: string
  subject_source:
    name: subject_source
    exact_mappings:
    - oa:hasBody
    from_schema: https://w3id.org/linkml/text_annotator
    slot_uri: sssom:subject_source
    alias: subject_source
    owner: HasSpan
    range: string
  subject_text_id:
    name: subject_text_id
    from_schema: https://w3id.org/linkml/text_annotator
    alias: subject_text_id
    owner: HasSpan
    range: TextualElement

```
</details>