# Class: AtomicQuery




URI: [search:AtomicQuery](https://w3id.org/linkml/search_datamodel/AtomicQuery)




```{mermaid}
 classDiagram
    class AtomicQuery
      AtomicQuery : graph_function
      AtomicQuery : graph_predicates
      AtomicQuery : search_term
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [graph_function](graph_function.md) | [GraphFunction](GraphFunction.md) | 0..1 | None  | . |
| [graph_predicates](graph_predicates.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..* | None  | . |
| [search_term](search_term.md) | [SearchBaseConfiguration](SearchBaseConfiguration.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [BooleanQuery](BooleanQuery.md) | [atom](atom.md) | range | AtomicQuery |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/search_datamodel







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['search:AtomicQuery'] |
| native | ['search:AtomicQuery'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: AtomicQuery
from_schema: https://w3id.org/linkml/search_datamodel
attributes:
  graph_function:
    name: graph_function
    from_schema: https://w3id.org/linkml/search_datamodel
    range: GraphFunction
  graph_predicates:
    name: graph_predicates
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true
    range: uriorcurie
  search_term:
    name: search_term
    from_schema: https://w3id.org/linkml/search_datamodel
    range: SearchBaseConfiguration

```
</details>

### Induced

<details>
```yaml
name: AtomicQuery
from_schema: https://w3id.org/linkml/search_datamodel
attributes:
  graph_function:
    name: graph_function
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: graph_function
    owner: AtomicQuery
    range: GraphFunction
  graph_predicates:
    name: graph_predicates
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true
    alias: graph_predicates
    owner: AtomicQuery
    range: uriorcurie
  search_term:
    name: search_term
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: search_term
    owner: AtomicQuery
    range: SearchBaseConfiguration

```
</details>