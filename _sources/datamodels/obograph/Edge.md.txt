# Class: Edge



URI: [og:Edge](https://github.com/geneontology/obographs/Edge)


```{mermaid}
 classDiagram
    class Edge
      Edge : obj
      Edge : pred
      Edge : sub
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [sub](sub.md) | 0..1 <br/> string | None | direct |
| [pred](pred.md) | 0..1 <br/> string | None | direct |
| [obj](obj.md) | 0..1 <br/> string | None | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [edges](edges.md) | range | Edge |







## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | og:Edge |
| native | og:Edge |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Edge
from_schema: https://github.com/geneontology/obographs
rank: 1000
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
rank: 1000
attributes:
  sub:
    name: sub
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: sub
    owner: Edge
    domain_of:
    - Edge
    range: string
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: pred
    owner: Edge
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: string
  obj:
    name: obj
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: obj
    owner: Edge
    domain_of:
    - Edge
    range: string

```
</details>