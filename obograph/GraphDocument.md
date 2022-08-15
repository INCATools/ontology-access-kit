# Class: GraphDocument




URI: [og:GraphDocument](https://github.com/geneontology/obographs/GraphDocument)




```{mermaid}
 classDiagram
    class GraphDocument
      GraphDocument : graphs
      GraphDocument : meta
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md)  |   |
| [graphs](graphs.md) | 0..* <br/> [Graph](Graph.md)  |   |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:GraphDocument'] |
| native | ['og:GraphDocument'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: GraphDocument
from_schema: https://github.com/geneontology/obographs
rank: 1000
slots:
- meta
- graphs

```
</details>

### Induced

<details>
```yaml
name: GraphDocument
from_schema: https://github.com/geneontology/obographs
rank: 1000
attributes:
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: GraphDocument
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta
  graphs:
    name: graphs
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: graphs
    owner: GraphDocument
    domain_of:
    - GraphDocument
    range: Graph
    inlined: true
    inlined_as_list: true

```
</details>