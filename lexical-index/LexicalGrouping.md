

# Class: LexicalGrouping


_A grouping of ontology elements by a shared lexical term_





URI: [ontolexindex:LexicalGrouping](https://w3id.org/oak/lexical-index/LexicalGrouping)






```{mermaid}
 classDiagram
    class LexicalGrouping
    click LexicalGrouping href "../LexicalGrouping"
      LexicalGrouping : relationships
        
          
    
    
    LexicalGrouping --> "*" RelationshipToTerm : relationships
    click RelationshipToTerm href "../RelationshipToTerm"

        
      LexicalGrouping : term
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [term](term.md) | 0..1 <br/> [String](String.md) | A normalized term that groups ontology elements | direct |
| [relationships](relationships.md) | * <br/> [RelationshipToTerm](RelationshipToTerm.md) | All ontology elements grouped and their relationship to the normalized term | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LexicalIndex](LexicalIndex.md) | [groupings](groupings.md) | range | [LexicalGrouping](LexicalGrouping.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/lexical-index




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontolexindex:LexicalGrouping |
| native | ontolexindex:LexicalGrouping |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LexicalGrouping
description: A grouping of ontology elements by a shared lexical term
from_schema: https://w3id.org/oak/lexical-index
attributes:
  term:
    name: term
    description: A normalized term that groups ontology elements
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    key: true
    domain_of:
    - LexicalGrouping
    required: true
  relationships:
    name: relationships
    description: All ontology elements grouped and their relationship to the normalized
      term
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    domain_of:
    - LexicalGrouping
    range: RelationshipToTerm
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: LexicalGrouping
description: A grouping of ontology elements by a shared lexical term
from_schema: https://w3id.org/oak/lexical-index
attributes:
  term:
    name: term
    description: A normalized term that groups ontology elements
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    key: true
    alias: term
    owner: LexicalGrouping
    domain_of:
    - LexicalGrouping
    range: string
    required: true
  relationships:
    name: relationships
    description: All ontology elements grouped and their relationship to the normalized
      term
    from_schema: https://w3id.org/oak/lexical-index
    rank: 1000
    alias: relationships
    owner: LexicalGrouping
    domain_of:
    - LexicalGrouping
    range: RelationshipToTerm
    multivalued: true

```
</details>