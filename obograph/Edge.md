

# Class: Edge


_An edge is a simple typed relationship between two nodes. When mapping to OWL, an edge represents either (a) s SubClassOf o (b) s SubClassOf p some o (c) s p o (where s and o are individuals) (d) s SubPropertyOf o (e) s EquivalentTo o (f) s type o_





URI: [obographs:Edge](https://github.com/geneontology/obographs/Edge)






```{mermaid}
 classDiagram
    class Edge
    click Edge href "../Edge"
      Edge : meta
        
          
    
    
    Edge --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      Edge : obj
        
      Edge : pred
        
      Edge : sub
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [sub](sub.md) | 1 <br/> [String](String.md) | the subject of an edge | direct |
| [pred](pred.md) | 1 <br/> [String](String.md) | the predicate of an edge | direct |
| [obj](obj.md) | 1 <br/> [String](String.md) | the object of an edge | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [edges](edges.md) | range | [Edge](Edge.md) |
| [Graph](Graph.md) | [allValuesFromEdges](allValuesFromEdges.md) | range | [Edge](Edge.md) |
| [DomainRangeAxiom](DomainRangeAxiom.md) | [allValuesFromEdges](allValuesFromEdges.md) | range | [Edge](Edge.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:Edge |
| native | obographs:Edge |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Edge
description: An edge is a simple typed relationship between two nodes. When mapping
  to OWL, an edge represents either (a) s SubClassOf o (b) s SubClassOf p some o (c)
  s p o (where s and o are individuals) (d) s SubPropertyOf o (e) s EquivalentTo o
  (f) s type o
from_schema: https://github.com/geneontology/obographs
slots:
- sub
- pred
- obj
- meta
slot_usage:
  sub:
    name: sub
    required: true
  pred:
    name: pred
    required: true
  obj:
    name: obj
    required: true

```
</details>

### Induced

<details>
```yaml
name: Edge
description: An edge is a simple typed relationship between two nodes. When mapping
  to OWL, an edge represents either (a) s SubClassOf o (b) s SubClassOf p some o (c)
  s p o (where s and o are individuals) (d) s SubPropertyOf o (e) s EquivalentTo o
  (f) s type o
from_schema: https://github.com/geneontology/obographs
slot_usage:
  sub:
    name: sub
    required: true
  pred:
    name: pred
    required: true
  obj:
    name: obj
    required: true
attributes:
  sub:
    name: sub
    description: the subject of an edge
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - subject
    - source
    - child
    - head
    rank: 1000
    slot_uri: rdf:subject
    alias: sub
    owner: Edge
    domain_of:
    - Edge
    range: string
    required: true
  pred:
    name: pred
    description: the predicate of an edge
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:predicate
    alias: pred
    owner: Edge
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - SynonymTypeDefinition
    range: string
    required: true
  obj:
    name: obj
    description: the object of an edge
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - object
    - target
    - parent
    - tail
    rank: 1000
    slot_uri: rdf:object
    alias: obj
    owner: Edge
    domain_of:
    - Edge
    range: string
    required: true
  meta:
    name: meta
    description: A collection of metadata about either an ontology (graph), an entity,
      or an axiom
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - annotations
    rank: 1000
    alias: meta
    owner: Edge
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - Edge
    - PropertyValue
    - Axiom
    range: Meta

```
</details>