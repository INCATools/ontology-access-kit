# Class: Node



URI: [rdf:Resource](http://www.w3.org/1999/02/22-rdf-syntax-ns#Resource)


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

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> string | None | direct |
| [lbl](lbl.md) | 0..1 <br/> string | None | direct |
| [type](type.md) | 0..1 <br/> string | None | direct |
| [meta](meta.md) | 0..1 <br/> Meta | None | direct |



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
| self | rdf:Resource |
| native | og:Node |


## LinkML Source

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
class_uri: rdf:Resource

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
class_uri: rdf:Resource

```
</details>