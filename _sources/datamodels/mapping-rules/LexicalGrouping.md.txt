# Class: LexicalGrouping
_A grouping of ontology elements by a shared lexical term_





URI: [li:LexicalGrouping](https://w3id.org/linkml/lexical_index/LexicalGrouping)




```{mermaid}
 classDiagram
    class LexicalGrouping
      LexicalGrouping : relationships
      LexicalGrouping : term
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [term](term.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | A normalized term that groups ontology elements  | . |
| [relationships](relationships.md) | [RelationshipToTerm](RelationshipToTerm.md) | 0..* | All ontology elements grouped and their relationship to the normalized term  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalIndex](LexicalIndex.md) | [groupings](groupings.md) | range | LexicalGrouping |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/lexical_index







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['li:LexicalGrouping'] |
| native | ['li:LexicalGrouping'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalGrouping
description: A grouping of ontology elements by a shared lexical term
from_schema: https://w3id.org/linkml/lexical_index
attributes:
  term:
    name: term
    description: A normalized term that groups ontology elements
    from_schema: https://w3id.org/linkml/lexical_index
    key: true
  relationships:
    name: relationships
    description: All ontology elements grouped and their relationship to the normalized
      term
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    range: RelationshipToTerm

```
</details>

### Induced

<details>
```yaml
name: LexicalGrouping
description: A grouping of ontology elements by a shared lexical term
from_schema: https://w3id.org/linkml/lexical_index
attributes:
  term:
    name: term
    description: A normalized term that groups ontology elements
    from_schema: https://w3id.org/linkml/lexical_index
    key: true
    alias: term
    owner: LexicalGrouping
    range: string
  relationships:
    name: relationships
    description: All ontology elements grouped and their relationship to the normalized
      term
    from_schema: https://w3id.org/linkml/lexical_index
    multivalued: true
    alias: relationships
    owner: LexicalGrouping
    range: RelationshipToTerm

```
</details>