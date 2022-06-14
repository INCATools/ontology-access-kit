# Class: RelationshipToTerm
_A relationship of an ontology element to a lexical term_





URI: [li:RelationshipToTerm](https://w3id.org/linkml/lexical_index/RelationshipToTerm)




```{mermaid}
 classDiagram
    class RelationshipToTerm
      RelationshipToTerm : element
      RelationshipToTerm : element_term
      RelationshipToTerm : pipeline
      RelationshipToTerm : predicate
      RelationshipToTerm : source
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [predicate](predicate.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..1 | None  | . |
| [element](element.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..1 | None  | . |
| [element_term](element_term.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | the original term used in the element  | . |
| [source](source.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..1 | None  | . |
| [pipeline](pipeline.md) | [LexicalTransformationPipeline](LexicalTransformationPipeline.md) | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalGrouping](LexicalGrouping.md) | [relationships](relationships.md) | range | RelationshipToTerm |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/lexical_index







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['li:RelationshipToTerm'] |
| native | ['li:RelationshipToTerm'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RelationshipToTerm
description: A relationship of an ontology element to a lexical term
from_schema: https://w3id.org/linkml/lexical_index
attributes:
  predicate:
    name: predicate
    from_schema: https://w3id.org/linkml/lexical_index
    range: uriorcurie
  element:
    name: element
    from_schema: https://w3id.org/linkml/lexical_index
    range: uriorcurie
  element_term:
    name: element_term
    description: the original term used in the element
    from_schema: https://w3id.org/linkml/lexical_index
  source:
    name: source
    from_schema: https://w3id.org/linkml/lexical_index
    range: uriorcurie
  pipeline:
    name: pipeline
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    range: LexicalTransformationPipeline

```
</details>

### Induced

<details>
```yaml
name: RelationshipToTerm
description: A relationship of an ontology element to a lexical term
from_schema: https://w3id.org/linkml/lexical_index
attributes:
  predicate:
    name: predicate
    from_schema: https://w3id.org/linkml/lexical_index
    alias: predicate
    owner: RelationshipToTerm
    range: uriorcurie
  element:
    name: element
    from_schema: https://w3id.org/linkml/lexical_index
    alias: element
    owner: RelationshipToTerm
    range: uriorcurie
  element_term:
    name: element_term
    description: the original term used in the element
    from_schema: https://w3id.org/linkml/lexical_index
    alias: element_term
    owner: RelationshipToTerm
    range: string
  source:
    name: source
    from_schema: https://w3id.org/linkml/lexical_index
    alias: source
    owner: RelationshipToTerm
    range: uriorcurie
  pipeline:
    name: pipeline
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    alias: pipeline
    owner: RelationshipToTerm
    range: LexicalTransformationPipeline

```
</details>