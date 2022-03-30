# Class: Edge




URI: [og:Edge](https://github.com/geneontology/obographs/Edge)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [sub](sub.md) | [string](string.md) | 0..1 | None  | . |
| [pred](pred.md) | [string](string.md) | 0..1 | None  | . |
| [obj](obj.md) | [string](string.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [edges](edges.md) | range | Edge |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Edge
from_schema: https://github.com/geneontology/obographs
slots:
- sub
- pred
- obj

```
</details>

### Induced

<details>
```yaml
name: Edge
from_schema: https://github.com/geneontology/obographs
attributes:
  sub:
    name: sub
    from_schema: https://github.com/geneontology/obographs
    alias: sub
    owner: Edge
    range: string
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    alias: pred
    owner: Edge
    range: string
  obj:
    name: obj
    from_schema: https://github.com/geneontology/obographs
    alias: obj
    owner: Edge
    range: string

```
</details>