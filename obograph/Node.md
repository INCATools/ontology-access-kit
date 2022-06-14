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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [lbl](lbl.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [type](type.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


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
attributes:
  id:
    name: id
    from_schema: https://github.com/geneontology/obographs
    identifier: true
    alias: id
    owner: Node
    range: string
  lbl:
    name: lbl
    from_schema: https://github.com/geneontology/obographs
    alias: lbl
    owner: Node
    range: string
  type:
    name: type
    from_schema: https://github.com/geneontology/obographs
    alias: type
    owner: Node
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: Node
    range: Meta

```
</details>