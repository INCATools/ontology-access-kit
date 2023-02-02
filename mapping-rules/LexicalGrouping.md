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

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [term](term.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | A normalized term that groups ontology elements | direct |
| [relationships](relationships.md) | 0..* <br/> [RelationshipToTerm](RelationshipToTerm.md) | All ontology elements grouped and their relationship to the normalized term | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalIndex](LexicalIndex.md) | [groupings](groupings.md) | range | [LexicalGrouping](LexicalGrouping.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/lexical_index





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | li:LexicalGrouping |
| native | li:LexicalGrouping |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalGrouping
description: A grouping of ontology elements by a shared lexical term
from_schema: https://w3id.org/linkml/lexical_index
rank: 1000
attributes:
  term:
    name: term
    description: A normalized term that groups ontology elements
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    key: true
  relationships:
    name: relationships
    description: All ontology elements grouped and their relationship to the normalized
      term
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
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
rank: 1000
attributes:
  term:
    name: term
    description: A normalized term that groups ontology elements
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    key: true
    alias: term
    owner: LexicalGrouping
    domain_of:
    - LexicalGrouping
    range: string
  relationships:
    name: relationships
    description: All ontology elements grouped and their relationship to the normalized
      term
    from_schema: https://w3id.org/linkml/lexical_index
    rank: 1000
    multivalued: true
    alias: relationships
    owner: LexicalGrouping
    domain_of:
    - LexicalGrouping
    range: RelationshipToTerm

```
</details>