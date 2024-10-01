

# Class: TextualElement



URI: [ann:TextualElement](https://w3id.org/linkml/text_annotator/TextualElement)






```{mermaid}
 classDiagram
    class TextualElement
    click TextualElement href "../TextualElement"
      TextualElement : id
        
      TextualElement : parent_document
        
      TextualElement : source_text
        
      TextualElement : text
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [text](text.md) | 0..1 <br/> [String](String.md) |  | direct |
| [source_text](source_text.md) | 0..1 <br/> [String](String.md) |  | direct |
| [parent_document](parent_document.md) | 0..1 <br/> [Uriorcurie](Uriorcurie.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [HasSpan](HasSpan.md) | [subject_text_id](subject_text_id.md) | range | [TextualElement](TextualElement.md) |
| [TextAnnotation](TextAnnotation.md) | [subject_text_id](subject_text_id.md) | range | [TextualElement](TextualElement.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




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
from_schema: https://w3id.org/oak/text_annotator
attributes:
  id:
    name: id
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    identifier: true
    domain_of:
    - TextualElement
    range: uriorcurie
    required: true
  text:
    name: text
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextualElement
    range: string
  source_text:
    name: source_text
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextualElement
    range: string
  parent_document:
    name: parent_document
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - TextualElement
    range: uriorcurie

```
</details>

### Induced

<details>
```yaml
name: TextualElement
from_schema: https://w3id.org/oak/text_annotator
attributes:
  id:
    name: id
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    identifier: true
    alias: id
    owner: TextualElement
    domain_of:
    - TextualElement
    range: uriorcurie
    required: true
  text:
    name: text
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: text
    owner: TextualElement
    domain_of:
    - TextualElement
    range: string
  source_text:
    name: source_text
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: source_text
    owner: TextualElement
    domain_of:
    - TextualElement
    range: string
  parent_document:
    name: parent_document
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: parent_document
    owner: TextualElement
    domain_of:
    - TextualElement
    range: uriorcurie

```
</details>