# Class: GraphDocument




URI: [og:GraphDocument](https://github.com/geneontology/obographs/GraphDocument)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |
| [graphs](graphs.md) | [Graph](Graph.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: GraphDocument
from_schema: https://github.com/geneontology/obographs
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
attributes:
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: GraphDocument
    range: Meta
  graphs:
    name: graphs
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    inlined: true
    inlined_as_list: true
    alias: graphs
    owner: GraphDocument
    range: Graph

```
</details>