# Class: Graph




URI: [og:Graph](https://github.com/geneontology/obographs/Graph)




```{mermaid}
 classDiagram
    class Graph
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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [lbl](lbl.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |
| [nodes](nodes.md) | [Node](Node.md) | 0..* | None  | . |
| [edges](edges.md) | [Edge](Edge.md) | 0..* | None  | . |
| [equivalentNodesSets](equivalentNodesSets.md) | [EquivalentNodesSet](EquivalentNodesSet.md) | 0..* | None  | . |
| [logicalDefinitionAxioms](logicalDefinitionAxioms.md) | [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | 0..* | None  | . |
| [domainRangeAxioms](domainRangeAxioms.md) | [DomainRangeAxiom](DomainRangeAxiom.md) | 0..* | None  | . |
| [propertyChainAxioms](propertyChainAxioms.md) | [PropertyChainAxiom](PropertyChainAxiom.md) | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GraphDocument](GraphDocument.md) | [graphs](graphs.md) | range | Graph |



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:Graph'] |
| native | ['og:Graph'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Graph
from_schema: https://github.com/geneontology/obographs
slots:
- id
- lbl
- meta
- nodes
- edges
- equivalentNodesSets
- logicalDefinitionAxioms
- domainRangeAxioms
- propertyChainAxioms

```
</details>

### Induced

<details>
```yaml
name: Graph
from_schema: https://github.com/geneontology/obographs
attributes:
  id:
    name: id
    from_schema: https://github.com/geneontology/obographs
    identifier: true
    alias: id
    owner: Graph
    range: string
  lbl:
    name: lbl
    from_schema: https://github.com/geneontology/obographs
    alias: lbl
    owner: Graph
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: Graph
    range: Meta
  nodes:
    name: nodes
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: nodes
    owner: Graph
    range: Node
    inlined: true
    inlined_as_list: true
  edges:
    name: edges
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: edges
    owner: Graph
    range: Edge
    inlined: true
    inlined_as_list: true
  equivalentNodesSets:
    name: equivalentNodesSets
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: equivalentNodesSets
    owner: Graph
    range: EquivalentNodesSet
  logicalDefinitionAxioms:
    name: logicalDefinitionAxioms
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: logicalDefinitionAxioms
    owner: Graph
    range: LogicalDefinitionAxiom
  domainRangeAxioms:
    name: domainRangeAxioms
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: domainRangeAxioms
    owner: Graph
    range: DomainRangeAxiom
  propertyChainAxioms:
    name: propertyChainAxioms
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: propertyChainAxioms
    owner: Graph
    range: PropertyChainAxiom

```
</details>