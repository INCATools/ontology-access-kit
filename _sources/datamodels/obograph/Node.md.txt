# Class: Node




URI: [og:Node](https://github.com/geneontology/obographs/Node)




```{mermaid}
 classDiagram
    class Node
      Node : id
      Node : lbl
      Node : meta
      Node : type
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [id](id.md) | 1..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [lbl](lbl.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [type](type.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md)  |   |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [nodes](nodes.md) | range | Node |



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:Node'] |
| native | ['og:Node'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Node
from_schema: https://github.com/geneontology/obographs
rank: 1000
slots:
- id
- lbl
- type
- meta

```
</details>

### Induced

<details>
```yaml
name: Node
from_schema: https://github.com/geneontology/obographs
rank: 1000
attributes:
  id:
    name: id
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    identifier: true
    alias: id
    owner: Node
    domain_of:
    - Graph
    - Node
    range: string
  lbl:
    name: lbl
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: lbl
    owner: Node
    domain_of:
    - Graph
    - Node
    range: string
  type:
    name: type
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: type
    owner: Node
    domain_of:
    - Node
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: Node
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta

```
</details>