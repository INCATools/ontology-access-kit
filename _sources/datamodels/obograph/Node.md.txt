# Class: Node




URI: [og:Node](https://github.com/geneontology/obographs/Node)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | [string](string.md) | 0..1 | None  | . |
| [label](label.md) | [string](string.md) | 0..1 | None  | . |
| [type](type.md) | [string](string.md) | 0..1 | None  | . |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [nodes](nodes.md) | range | Node |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Node
from_schema: https://github.com/geneontology/obographs
slots:
- id
- label
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
  label:
    name: label
    from_schema: https://github.com/geneontology/obographs
    alias: label
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