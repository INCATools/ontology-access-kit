# Class: TextualElement



URI: [ann:TextualElement](https://w3id.org/linkml/text_annotator/TextualElement)


```{mermaid}
 classDiagram
    class TextualElement
      TextualElement : id
      TextualElement : parent_document
      TextualElement : source_text
      TextualElement : text
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> uriorcurie | None | direct |
| [text](text.md) | 0..1 <br/> string | None | direct |
| [source_text](source_text.md) | 0..1 <br/> string | None | direct |
| [parent_document](parent_document.md) | 0..1 <br/> uriorcurie | None | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasSpan](HasSpan.md) | [subject_text_id](subject_text_id.md) | range | TextualElement |
| [TextAnnotation](TextAnnotation.md) | [subject_text_id](subject_text_id.md) | range | TextualElement |







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/text_annotator





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:TextualElement |
| native | ann:TextualElement |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TextualElement
from_schema: https://w3id.org/linkml/text_annotator
rank: 1000
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    identifier: true
    range: uriorcurie
  text:
    name: text
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    range: string
  source_text:
    name: source_text
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    range: string
  parent_document:
    name: parent_document
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    range: uriorcurie

```
</details>

### Induced

<details>
```yaml
name: TextualElement
from_schema: https://w3id.org/linkml/text_annotator
rank: 1000
attributes:
  id:
    name: id
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    identifier: true
    alias: id
    owner: TextualElement
    domain_of:
    - TextualElement
    range: uriorcurie
  text:
    name: text
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    alias: text
    owner: TextualElement
    domain_of:
    - TextualElement
    range: string
  source_text:
    name: source_text
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    alias: source_text
    owner: TextualElement
    domain_of:
    - TextualElement
    range: string
  parent_document:
    name: parent_document
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    alias: parent_document
    owner: TextualElement
    domain_of:
    - TextualElement
    range: uriorcurie

```
</details>