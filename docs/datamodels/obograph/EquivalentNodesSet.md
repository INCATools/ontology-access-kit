

# Class: EquivalentNodesSet


_A clique of nodes that are all mutually equivalent_





URI: [owl:equivalentClass](http://www.w3.org/2002/07/owl#equivalentClass)






```{mermaid}
 classDiagram
    class EquivalentNodesSet
    click EquivalentNodesSet href "../EquivalentNodesSet"
      Axiom <|-- EquivalentNodesSet
        click Axiom href "../Axiom"
      
      EquivalentNodesSet : meta
        
          
    
    
    EquivalentNodesSet --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      EquivalentNodesSet : nodeIds
        
      EquivalentNodesSet : representativeNodeId
        
      
```





## Inheritance
* [Axiom](Axiom.md)
    * **EquivalentNodesSet**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [representativeNodeId](representativeNodeId.md) | 0..1 <br/> [String](String.md) | The identifier of a node that represents the class in an OWL equivalence cliq... | direct |
| [nodeIds](nodeIds.md) | * <br/> [String](String.md) |  | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [Axiom](Axiom.md) |





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
| native | obographs:EquivalentNodesSet |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: EquivalentNodesSet
description: A clique of nodes that are all mutually equivalent
from_schema: https://github.com/geneontology/obographs
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
description: A clique of nodes that are all mutually equivalent
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
attributes:
  representativeNodeId:
    name: representativeNodeId
    description: The identifier of a node that represents the class in an OWL equivalence
      clique
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
    alias: nodeIds
    owner: EquivalentNodesSet
    domain_of:
    - EquivalentNodesSet
    range: string
    multivalued: true
  meta:
    name: meta
    description: A collection of metadata about either an ontology (graph), an entity,
      or an axiom
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - annotations
    rank: 1000
    alias: meta
    owner: EquivalentNodesSet
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - Edge
    - PropertyValue
    - Axiom
    range: Meta
class_uri: owl:equivalentClass

```
</details>