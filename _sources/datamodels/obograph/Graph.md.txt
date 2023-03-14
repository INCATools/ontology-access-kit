# Class: Graph
_A graph is a collection of nodes and edges and other axioms that represents a single ontology._




URI: [owl:Ontology](http://www.w3.org/2002/07/owl#Ontology)



```{mermaid}
 classDiagram
    class Graph
      Graph : allValuesFromEdges
        
          Graph ..> Edge : allValuesFromEdges
        
      Graph : domainRangeAxioms
        
          Graph ..> DomainRangeAxiom : domainRangeAxioms
        
      Graph : edges
        
          Graph ..> Edge : edges
        
      Graph : equivalentNodesSets
        
          Graph ..> EquivalentNodesSet : equivalentNodesSets
        
      Graph : id
        
      Graph : lbl
        
      Graph : logicalDefinitionAxioms
        
          Graph ..> LogicalDefinitionAxiom : logicalDefinitionAxioms
        
      Graph : meta
        
          Graph ..> Meta : meta
        
      Graph : nodes
        
          Graph ..> Node : nodes
        
      Graph : prefixes
        
          Graph ..> PrefixDeclaration : prefixes
        
      Graph : propertyChainAxioms
        
          Graph ..> PropertyChainAxiom : propertyChainAxioms
        
      Graph : subsetDefinitions
        
          Graph ..> SubsetDefinition : subsetDefinitions
        
      Graph : synonymTypeDefinitions
        
          Graph ..> SynonymTypeDefinition : synonymTypeDefinitions
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [OboIdentifierString](OboIdentifierString.md) | The unique identifier of the entity | direct |
| [lbl](lbl.md) | 0..1 <br/> [String](String.md) | the human-readable label of a node | direct |
| [prefixes](prefixes.md) | 0..* <br/> [PrefixDeclaration](PrefixDeclaration.md) | A collection of mappings between prefixes and namespaces, used to map CURIEs ... | direct |
| [subsetDefinitions](subsetDefinitions.md) | 0..* <br/> [SubsetDefinition](SubsetDefinition.md) |  | direct |
| [synonymTypeDefinitions](synonymTypeDefinitions.md) | 0..* <br/> [SynonymTypeDefinition](SynonymTypeDefinition.md) |  | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | direct |
| [nodes](nodes.md) | 0..* <br/> [Node](Node.md) | All nodes present in a graph | direct |
| [edges](edges.md) | 0..* <br/> [Edge](Edge.md) | All edges present in a graph | direct |
| [equivalentNodesSets](equivalentNodesSets.md) | 0..* <br/> [EquivalentNodesSet](EquivalentNodesSet.md) | A list of sets of nodes that form equivalence cliques | direct |
| [logicalDefinitionAxioms](logicalDefinitionAxioms.md) | 0..* <br/> [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | A list of logical definition axioms that define the meaning of a class in ter... | direct |
| [domainRangeAxioms](domainRangeAxioms.md) | 0..* <br/> [DomainRangeAxiom](DomainRangeAxiom.md) | A list of axioms that define the domain and range of a property | direct |
| [allValuesFromEdges](allValuesFromEdges.md) | 0..* <br/> [Edge](Edge.md) | A list of edges that represent subclasses of universal restrictions | direct |
| [propertyChainAxioms](propertyChainAxioms.md) | 0..* <br/> [PropertyChainAxiom](PropertyChainAxiom.md) | A list of axioms that define an OWL property chain | direct |





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
| native | obographs:Graph |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Graph
description: A graph is a collection of nodes and edges and other axioms that represents
  a single ontology.
from_schema: https://github.com/geneontology/obographs
rank: 1000
slots:
- id
- lbl
- prefixes
- subsetDefinitions
- synonymTypeDefinitions
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
description: A graph is a collection of nodes and edges and other axioms that represents
  a single ontology.
from_schema: https://github.com/geneontology/obographs
rank: 1000
attributes:
  id:
    name: id
    description: The unique identifier of the entity
    from_schema: https://github.com/geneontology/obographs
    see_also:
    - https://owlcollab.github.io/oboformat/doc/obo-syntax.html#2.5
    rank: 1000
    identifier: true
    alias: id
    owner: Graph
    domain_of:
    - Graph
    - Node
    - SubsetDefinition
    - SynonymTypeDefinition
    range: OboIdentifierString
  lbl:
    name: lbl
    description: the human-readable label of a node
    comments:
    - the name "lbl" exists for legacy purposes, this should be considered identical
      to label in rdfs
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - label
    - name
    rank: 1000
    slot_uri: rdfs:label
    alias: lbl
    owner: Graph
    domain_of:
    - Graph
    - Node
    - SubsetDefinition
    - SynonymTypeDefinition
    range: string
  prefixes:
    name: prefixes
    description: A collection of mappings between prefixes and namespaces, used to
      map CURIEs (e.g. GO:0008150) to IRIs (e.g. http://purl.obolibrary.org/obo/GO_0008150)
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: sh:declare
    multivalued: true
    alias: prefixes
    owner: Graph
    domain_of:
    - GraphDocument
    - Graph
    range: PrefixDeclaration
    inlined: true
  subsetDefinitions:
    name: subsetDefinitions
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: subsetDefinitions
    owner: Graph
    domain_of:
    - Graph
    range: SubsetDefinition
    inlined: true
  synonymTypeDefinitions:
    name: synonymTypeDefinitions
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: synonymTypeDefinitions
    owner: Graph
    domain_of:
    - Graph
    range: SynonymTypeDefinition
    inlined: true
  meta:
    name: meta
    description: A collection of metadata about either an ontology (graph), an entity,
      or an axiom
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - annotations
    rank: 1000
    alias: meta
    owner: Graph
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - Edge
    - PropertyValue
    - Axiom
    range: Meta
  nodes:
    name: nodes
    description: All nodes present in a graph. This includes class nodes as well as
      supporting nodes, including nodes representing relationship types, subsets,
      annotation proeprties, etc
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
    description: All edges present in a graph.
    comments:
    - Note that this only includes core edges, formed by translating (a) SubClassOf
      between named classes (b) SubPropertyOf (c) SubClassOf between a named class
      and a simple existential axiom (d) ObjectPropertyAssertions
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
    description: A list of sets of nodes that form equivalence cliques
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
    description: A list of logical definition axioms that define the meaning of a
      class in terms of other classes.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: logicalDefinitionAxioms
    owner: Graph
    domain_of:
    - Graph
    range: LogicalDefinitionAxiom
    inlined: true
    inlined_as_list: true
  domainRangeAxioms:
    name: domainRangeAxioms
    description: A list of axioms that define the domain and range of a property
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
    - DomainRangeAxiom
    range: Edge
  propertyChainAxioms:
    name: propertyChainAxioms
    description: A list of axioms that define an OWL property chain
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