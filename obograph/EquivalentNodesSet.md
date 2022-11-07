# Class: EquivalentNodesSet



URI: [og:EquivalentNodesSet](https://github.com/geneontology/obographs/EquivalentNodesSet)


```{mermaid}
 classDiagram
    class EquivalentNodesSet
      Axiom <|-- EquivalentNodesSet
      
      EquivalentNodesSet : meta
      EquivalentNodesSet : nodeIds
      EquivalentNodesSet : representativeNodeId
      
```




## Inheritance
* [Axiom](Axiom.md)
    * **EquivalentNodesSet**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [representativeNodeId](representativeNodeId.md) | 0..1 <br/> string | None | direct |
| [nodeIds](nodeIds.md) | 0..* <br/> string | None | direct |
| [meta](meta.md) | 0..1 <br/> Meta | None | [Axiom](Axiom.md) |



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
| self | og:EquivalentNodesSet |
| native | og:EquivalentNodesSet |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: EquivalentNodesSet
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: Axiom
slots:
- representativeNodeId
- nodeIds

```
</details>

### Induced

<details>
```yaml
name: EquivalentNodesSet
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: Axiom
attributes:
  representativeNodeId:
    name: representativeNodeId
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: representativeNodeId
    owner: EquivalentNodesSet
    domain_of:
    - EquivalentNodesSet
    range: string
  nodeIds:
    name: nodeIds
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: nodeIds
    owner: EquivalentNodesSet
    domain_of:
    - EquivalentNodesSet
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: EquivalentNodesSet
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta

```
</details>