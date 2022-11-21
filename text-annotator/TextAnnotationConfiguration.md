# Class: TextAnnotationConfiguration
_configuration for search_




URI: [ann:TextAnnotationConfiguration](https://w3id.org/linkml/text_annotator/TextAnnotationConfiguration)


```{mermaid}
 classDiagram
    class TextAnnotationConfiguration
      TextAnnotationConfiguration : limit
      TextAnnotationConfiguration : matches_whole_text
      TextAnnotationConfiguration : sources
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [matches_whole_text](matches_whole_text.md) | 0..1 <br/> NONE |  | direct |
| [sources](sources.md) | 0..* <br/> NONE |  | direct |
| [limit](limit.md) | 0..1 <br/> [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) |  | direct |







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/text_annotator





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
from_schema: https://w3id.org/linkml/text_annotator
rank: 1000
attributes:
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    range: boolean
  sources:
    name: sources
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    multivalued: true
  limit:
    name: limit
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    range: integer

```
</details>

### Induced

<details>
```yaml
name: TextAnnotationConfiguration
description: configuration for search
from_schema: https://w3id.org/linkml/text_annotator
rank: 1000
attributes:
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    alias: matches_whole_text
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    - TextAnnotation
    range: boolean
  sources:
    name: sources
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    multivalued: true
    alias: sources
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: string
  limit:
    name: limit
    from_schema: https://w3id.org/linkml/text_annotator
    rank: 1000
    alias: limit
    owner: TextAnnotationConfiguration
    domain_of:
    - TextAnnotationConfiguration
    range: integer

```
</details>