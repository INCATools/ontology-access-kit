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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [matches_whole_text](matches_whole_text.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [sources](sources.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [limit](limit.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/text_annotator







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['ann:TextAnnotationConfiguration'] |
| native | ['ann:TextAnnotationConfiguration'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TextAnnotationConfiguration
description: configuration for search
from_schema: https://w3id.org/linkml/text_annotator
attributes:
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/linkml/text_annotator
    range: boolean
  sources:
    name: sources
    from_schema: https://w3id.org/linkml/text_annotator
    multivalued: true
  limit:
    name: limit
    from_schema: https://w3id.org/linkml/text_annotator
    range: integer

```
</details>

### Induced

<details>
```yaml
name: TextAnnotationConfiguration
description: configuration for search
from_schema: https://w3id.org/linkml/text_annotator
attributes:
  matches_whole_text:
    name: matches_whole_text
    from_schema: https://w3id.org/linkml/text_annotator
    alias: matches_whole_text
    owner: TextAnnotationConfiguration
    range: boolean
  sources:
    name: sources
    from_schema: https://w3id.org/linkml/text_annotator
    multivalued: true
    alias: sources
    owner: TextAnnotationConfiguration
    range: string
  limit:
    name: limit
    from_schema: https://w3id.org/linkml/text_annotator
    alias: limit
    owner: TextAnnotationConfiguration
    range: integer

```
</details>