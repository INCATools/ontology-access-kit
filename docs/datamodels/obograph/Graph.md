# Class: Graph



URI: [owl:Ontology](http://www.w3.org/2002/07/owl#Ontology)


```{mermaid}
 classDiagram
    class Graph
      Graph : allValuesFromEdges
      Graph : domainRangeAxioms
      Graph : edges
      Graph : equivalentNodesSets
      Graph : id
      Graph : lbl
      Graph : logicalDefinitionAxioms
      Graph : meta
      Graph : nodes
      Graph : propertyChainAxioms
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [lbl](lbl.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) |  | direct |
| [nodes](nodes.md) | 0..* <br/> [Node](Node.md) |  | direct |
| [edges](edges.md) | 0..* <br/> [Edge](Edge.md) |  | direct |
| [equivalentNodesSets](equivalentNodesSets.md) | 0..* <br/> [EquivalentNodesSet](EquivalentNodesSet.md) |  | direct |
| [logicalDefinitionAxioms](logicalDefinitionAxioms.md) | 0..* <br/> [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) |  | direct |
| [domainRangeAxioms](domainRangeAxioms.md) | 0..* <br/> [DomainRangeAxiom](DomainRangeAxiom.md) |  | direct |
| [allValuesFromEdges](allValuesFromEdges.md) | 0..* <br/> [Edge](Edge.md) | A list of edges that represent subclasses of universal restrictions | direct |
| [propertyChainAxioms](propertyChainAxioms.md) | 0..* <br/> [PropertyChainAxiom](PropertyChainAxiom.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GraphDocument](GraphDocument.md) | [graphs](graphs.md) | range | [Graph](Graph.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:Ontology |
| native | og:Graph |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Graph
from_schema: https://github.com/geneontology/obographs
rank: 1000
slots:
- id
- lbl
- meta
- nodes
- edges
- equivalentNodesSets
- logicalDefinitionAxioms
- domainRangeAxioms
- allValuesFromEdges
- propertyChainAxioms
class_uri: owl:Ontology

```
</details>

### Induced

<details>
```yaml
name: Graph
from_schema: https://github.com/geneontology/obographs
rank: 1000
attributes:
  id:
    name: id
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    identifier: true
    alias: id
    owner: Graph
    domain_of:
    - Graph
    - Node
    range: string
  lbl:
    name: lbl
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: lbl
    owner: Graph
    domain_of:
    - Graph
    - Node
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: Graph
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta
  nodes:
    name: nodes
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: nodes
    owner: Graph
    domain_of:
    - Graph
    range: Node
    inlined: true
    inlined_as_list: true
  edges:
    name: edges
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: edges
    owner: Graph
    domain_of:
    - Graph
    range: Edge
    inlined: true
    inlined_as_list: true
  equivalentNodesSets:
    name: equivalentNodesSets
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: equivalentNodesSets
    owner: Graph
    domain_of:
    - Graph
    range: EquivalentNodesSet
  logicalDefinitionAxioms:
    name: logicalDefinitionAxioms
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: logicalDefinitionAxioms
    owner: Graph
    domain_of:
    - Graph
    range: LogicalDefinitionAxiom
  domainRangeAxioms:
    name: domainRangeAxioms
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: domainRangeAxioms
    owner: Graph
    domain_of:
    - Graph
    range: DomainRangeAxiom
  allValuesFromEdges:
    name: allValuesFromEdges
    description: A list of edges that represent subclasses of universal restrictions
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: allValuesFromEdges
    owner: Graph
    domain_of:
    - Graph
    range: Edge
  propertyChainAxioms:
    name: propertyChainAxioms
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: propertyChainAxioms
    owner: Graph
    domain_of:
    - Graph
    range: PropertyChainAxiom
class_uri: owl:Ontology

```
</details>