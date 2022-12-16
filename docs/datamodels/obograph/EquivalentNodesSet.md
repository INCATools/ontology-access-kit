# Class: EquivalentNodesSet



URI: [owl:equivalentClass](http://www.w3.org/2002/07/owl#equivalentClass)


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
| [representativeNodeId](representativeNodeId.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [nodeIds](nodeIds.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) |  | [Axiom](Axiom.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [equivalentNodesSets](equivalentNodesSets.md) | range | [EquivalentNodesSet](EquivalentNodesSet.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:equivalentClass |
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
class_uri: owl:equivalentClass

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
class_uri: owl:equivalentClass

```
</details>