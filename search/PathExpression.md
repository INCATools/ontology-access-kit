# Class: PathExpression
_A path query_




URI: [search:PathExpression](https://w3id.org/linkml/search_datamodel/PathExpression)


```{mermaid}
 classDiagram
    class PathExpression
      PathExpression : graph_predicates
      PathExpression : search_term
      PathExpression : traversal
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [traversal](traversal.md) | 0..1 <br/> GraphFunction | None | direct |
| [graph_predicates](graph_predicates.md) | 0..* <br/> uriorcurie | None | direct |
| [search_term](search_term.md) | 0..1 <br/> SearchBaseConfiguration | None | direct |








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/search_datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | search:PathExpression |
| native | search:PathExpression |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PathExpression
description: A path query
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
attributes:
  traversal:
    name: traversal
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: GraphFunction
  graph_predicates:
    name: graph_predicates
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    range: uriorcurie
  search_term:
    name: search_term
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: SearchBaseConfiguration

```
</details>

### Induced

<details>
```yaml
name: PathExpression
description: A path query
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
attributes:
  traversal:
    name: traversal
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: traversal
    owner: PathExpression
    domain_of:
    - PathExpression
    range: GraphFunction
  graph_predicates:
    name: graph_predicates
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    alias: graph_predicates
    owner: PathExpression
    domain_of:
    - PathExpression
    range: uriorcurie
  search_term:
    name: search_term
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: search_term
    owner: PathExpression
    domain_of:
    - PathExpression
    range: SearchBaseConfiguration

```
</details>