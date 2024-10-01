

# Class: HasSpan



URI: [ann:HasSpan](https://w3id.org/linkml/text_annotator/HasSpan)






```{mermaid}
 classDiagram
    class HasSpan
    click HasSpan href "../HasSpan"
      HasSpan <|-- TextAnnotation
        click TextAnnotation href "../TextAnnotation"
      
      HasSpan : subject_end
        
      HasSpan : subject_label
        
      HasSpan : subject_source
        
      HasSpan : subject_start
        
      HasSpan : subject_text_id
        
          
    
    
    HasSpan --> "0..1" TextualElement : subject_text_id
    click TextualElement href "../TextualElement"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject_start](subject_start.md) | 0..1 <br/> [Position](Position.md) |  | direct |
| [subject_end](subject_end.md) | 0..1 <br/> [Position](Position.md) |  | direct |
| [subject_label](subject_label.md) | 0..1 <br/> [String](String.md) | The portion of the subject text that is matched, ranging from subject_start t... | direct |
| [subject_source](subject_source.md) | 0..1 <br/> [String](String.md) |  | direct |
| [subject_text_id](subject_text_id.md) | 0..1 <br/> [TextualElement](TextualElement.md) |  | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [TextAnnotation](TextAnnotation.md) | An individual text annotation |








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/text_annotator




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ann:HasSpan |
| native | ann:HasSpan |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasSpan
from_schema: https://w3id.org/oak/text_annotator
mixin: true
attributes:
  subject_start:
    name: subject_start
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:from
    rank: 1000
    domain_of:
    - HasSpan
    range: Position
  subject_end:
    name: subject_end
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:to
    rank: 1000
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
    domain_of:
    - HasSpan
  subject_source:
    name: subject_source
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - oa:hasBody
    rank: 1000
    slot_uri: sssom:subject_source
    domain_of:
    - HasSpan
  subject_text_id:
    name: subject_text_id
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    domain_of:
    - HasSpan
    range: TextualElement

```
</details>

### Induced

<details>
```yaml
name: HasSpan
from_schema: https://w3id.org/oak/text_annotator
mixin: true
attributes:
  subject_start:
    name: subject_start
    from_schema: https://w3id.org/oak/text_annotator
    exact_mappings:
    - bpa:from
    rank: 1000
    alias: subject_start
    owner: HasSpan
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
    owner: HasSpan
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
    owner: HasSpan
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
    owner: HasSpan
    domain_of:
    - HasSpan
    range: string
  subject_text_id:
    name: subject_text_id
    from_schema: https://w3id.org/oak/text_annotator
    rank: 1000
    alias: subject_text_id
    owner: HasSpan
    domain_of:
    - HasSpan
    range: TextualElement

```
</details>