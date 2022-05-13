# Class: TextualElement




URI: [ann:TextualElement](https://w3id.org/linkml/text_annotator/TextualElement)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | [uriorcurie](uriorcurie.md) | 0..1 | None  | . |
| [text](text.md) | [string](string.md) | 0..1 | None  | . |
| [source_text](source_text.md) | [string](string.md) | 0..1 | None  | . |
| [parent_document](parent_document.md) | [uriorcurie](uriorcurie.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasSpan](HasSpan.md) | [subject_text_id](subject_text_id.md) | range | TextualElement |
| [TextAnnotation](TextAnnotation.md) | [subject_text_id](subject_text_id.md) | range | TextualElement |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TextualElement
from_schema: https://w3id.org/linkml/text_annotator
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/text_annotator
    identifier: true
    range: uriorcurie
  text:
    name: text
    from_schema: https://w3id.org/linkml/text_annotator
    range: string
  source_text:
    name: source_text
    from_schema: https://w3id.org/linkml/text_annotator
    range: string
  parent_document:
    name: parent_document
    from_schema: https://w3id.org/linkml/text_annotator
    range: uriorcurie

```
</details>

### Induced

<details>
```yaml
name: TextualElement
from_schema: https://w3id.org/linkml/text_annotator
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/text_annotator
    identifier: true
    alias: id
    owner: TextualElement
    range: uriorcurie
  text:
    name: text
    from_schema: https://w3id.org/linkml/text_annotator
    alias: text
    owner: TextualElement
    range: string
  source_text:
    name: source_text
    from_schema: https://w3id.org/linkml/text_annotator
    alias: source_text
    owner: TextualElement
    range: string
  parent_document:
    name: parent_document
    from_schema: https://w3id.org/linkml/text_annotator
    alias: parent_document
    owner: TextualElement
    range: uriorcurie

```
</details>