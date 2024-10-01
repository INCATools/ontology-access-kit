

# Class: Node


_A node is a class, property, or other entity in an ontology_





URI: [rdf:Resource](http://www.w3.org/1999/02/22-rdf-syntax-ns#Resource)






```{mermaid}
 classDiagram
    class Node
    click Node href "../Node"
      Node : id
        
      Node : lbl
        
      Node : meta
        
          
    
    
    Node --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      Node : propertyType
        
          
    
    
    Node --> "0..1" PropertyTypeEnum : propertyType
    click PropertyTypeEnum href "../PropertyTypeEnum"

        
      Node : type
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1 <br/> [OboIdentifierString](OboIdentifierString.md) | The unique identifier of the entity | direct |
| [lbl](lbl.md) | 0..1 <br/> [String](String.md) | the human-readable label of a node | direct |
| [type](type.md) | 0..1 <br/> [String](String.md) |  | direct |
| [propertyType](propertyType.md) | 0..1 <br/> [PropertyTypeEnum](PropertyTypeEnum.md) |  | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [nodes](nodes.md) | range | [Node](Node.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdf:Resource |
| native | obographs:Node |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Node
description: A node is a class, property, or other entity in an ontology
from_schema: https://github.com/geneontology/obographs
slots:
- id
- lbl
- type
- propertyType
- meta
class_uri: rdf:Resource

```
</details>

### Induced

<details>
```yaml
name: Node
description: A node is a class, property, or other entity in an ontology
from_schema: https://github.com/geneontology/obographs
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
    owner: Node
    domain_of:
    - Graph
    - Node
    - SubsetDefinition
    - SynonymTypeDefinition
    range: OboIdentifierString
    required: true
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
    owner: Node
    domain_of:
    - Graph
    - Node
    - SubsetDefinition
    - SynonymTypeDefinition
    range: string
  type:
    name: type
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: type
    owner: Node
    domain_of:
    - Node
    range: string
  propertyType:
    name: propertyType
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: propertyType
    owner: Node
    domain_of:
    - Node
    range: PropertyTypeEnum
  meta:
    name: meta
    description: A collection of metadata about either an ontology (graph), an entity,
      or an axiom
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - annotations
    rank: 1000
    alias: meta
    owner: Node
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - Edge
    - PropertyValue
    - Axiom
    range: Meta
class_uri: rdf:Resource

```
</details>