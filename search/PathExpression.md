

# Class: PathExpression


_A path query_





URI: [ontosearch:PathExpression](https://w3id.org/oak/search-datamodel/PathExpression)






```{mermaid}
 classDiagram
    class PathExpression
    click PathExpression href "../PathExpression"
      PathExpression : graph_predicates
        
      PathExpression : search_term
        
          
    
    
    PathExpression --> "0..1" SearchBaseConfiguration : search_term
    click SearchBaseConfiguration href "../SearchBaseConfiguration"

        
      PathExpression : traversal
        
          
    
    
    PathExpression --> "0..1" GraphFunction : traversal
    click GraphFunction href "../GraphFunction"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [traversal](traversal.md) | 0..1 <br/> [GraphFunction](GraphFunction.md) |  | direct |
| [graph_predicates](graph_predicates.md) | * <br/> [Uriorcurie](Uriorcurie.md) |  | direct |
| [search_term](search_term.md) | 0..1 <br/> [SearchBaseConfiguration](SearchBaseConfiguration.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/search-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ontosearch:PathExpression |
| native | ontosearch:PathExpression |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PathExpression
description: A path query
from_schema: https://w3id.org/oak/search-datamodel
attributes:
  traversal:
    name: traversal
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - PathExpression
    range: GraphFunction
  graph_predicates:
    name: graph_predicates
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - PathExpression
    range: uriorcurie
    multivalued: true
  search_term:
    name: search_term
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    domain_of:
    - PathExpression
    range: SearchBaseConfiguration

```
</details>

### Induced

<details>
```yaml
name: PathExpression
description: A path query
from_schema: https://w3id.org/oak/search-datamodel
attributes:
  traversal:
    name: traversal
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: traversal
    owner: PathExpression
    domain_of:
    - PathExpression
    range: GraphFunction
  graph_predicates:
    name: graph_predicates
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: graph_predicates
    owner: PathExpression
    domain_of:
    - PathExpression
    range: uriorcurie
    multivalued: true
  search_term:
    name: search_term
    from_schema: https://w3id.org/oak/search-datamodel
    rank: 1000
    alias: search_term
    owner: PathExpression
    domain_of:
    - PathExpression
    range: SearchBaseConfiguration

```
</details>