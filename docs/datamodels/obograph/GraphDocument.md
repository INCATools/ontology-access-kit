

# Class: GraphDocument


_A graph document is a collection of graphs together with a set of prefixes that apply across all of them_





URI: [obographs:GraphDocument](https://github.com/geneontology/obographs/GraphDocument)






```{mermaid}
 classDiagram
    class GraphDocument
    click GraphDocument href "../GraphDocument"
      GraphDocument : graphs
        
          
    
    
    GraphDocument --> "*" Graph : graphs
    click Graph href "../Graph"

        
      GraphDocument : meta
        
          
    
    
    GraphDocument --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      GraphDocument : prefixes
        
          
    
    
    GraphDocument --> "*" PrefixDeclaration : prefixes
    click PrefixDeclaration href "../PrefixDeclaration"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | direct |
| [graphs](graphs.md) | * <br/> [Graph](Graph.md) | A list of all graphs (ontologies) in an ontology document | direct |
| [prefixes](prefixes.md) | * <br/> [PrefixDeclaration](PrefixDeclaration.md) | A collection of mappings between prefixes and namespaces, used to map CURIEs ... | direct |









## Comments

* A graph document frequently has a single graph but a multi-graph document can be used to represent multiple ontologies in an import closure in a single file.

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:GraphDocument |
| native | obographs:GraphDocument |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: GraphDocument
description: A graph document is a collection of graphs together with a set of prefixes
  that apply across all of them
comments:
- A graph document frequently has a single graph but a multi-graph document can be
  used to represent multiple ontologies in an import closure in a single file.
from_schema: https://github.com/geneontology/obographs
slots:
- meta
- graphs
- prefixes

```
</details>

### Induced

<details>
```yaml
name: GraphDocument
description: A graph document is a collection of graphs together with a set of prefixes
  that apply across all of them
comments:
- A graph document frequently has a single graph but a multi-graph document can be
  used to represent multiple ontologies in an import closure in a single file.
from_schema: https://github.com/geneontology/obographs
attributes:
  meta:
    name: meta
    description: A collection of metadata about either an ontology (graph), an entity,
      or an axiom
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - annotations
    rank: 1000
    alias: meta
    owner: GraphDocument
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - Edge
    - PropertyValue
    - Axiom
    range: Meta
  graphs:
    name: graphs
    description: A list of all graphs (ontologies) in an ontology document.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: graphs
    owner: GraphDocument
    domain_of:
    - GraphDocument
    range: Graph
    multivalued: true
    inlined: true
    inlined_as_list: true
  prefixes:
    name: prefixes
    description: A collection of mappings between prefixes and namespaces, used to
      map CURIEs (e.g. GO:0008150) to IRIs (e.g. http://purl.obolibrary.org/obo/GO_0008150)
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: sh:declare
    alias: prefixes
    owner: GraphDocument
    domain_of:
    - GraphDocument
    - Graph
    range: PrefixDeclaration
    multivalued: true
    inlined: true

```
</details>