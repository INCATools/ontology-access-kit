# Class: EquivalentNodesSet




URI: [og:EquivalentNodesSet](https://github.com/geneontology/obographs/EquivalentNodesSet)




```{mermaid}
 classDiagram
      Axiom <|-- EquivalentNodesSet
      
      EquivalentNodesSet : meta
      EquivalentNodesSet : nodeIds
      EquivalentNodesSet : representitiveNodeId
      

```





## Inheritance
* [Axiom](Axiom.md)
    * **EquivalentNodesSet**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [representitiveNodeId](representitiveNodeId.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [nodeIds](nodeIds.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [equivalentNodesSets](equivalentNodesSets.md) | range | EquivalentNodesSet |



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:EquivalentNodesSet'] |
| native | ['og:EquivalentNodesSet'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: EquivalentNodesSet
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
slots:
- representitiveNodeId
- nodeIds

```
</details>

### Induced

<details>
```yaml
name: EquivalentNodesSet
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
attributes:
  representitiveNodeId:
    name: representitiveNodeId
    from_schema: https://github.com/geneontology/obographs
    alias: representitiveNodeId
    owner: EquivalentNodesSet
    range: string
  nodeIds:
    name: nodeIds
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: nodeIds
    owner: EquivalentNodesSet
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: EquivalentNodesSet
    range: Meta

```
</details>