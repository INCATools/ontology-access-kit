

# Class: PropertyChainAxiom


_An axiom that represents an OWL property chain, e.g. R <- R1 o ... o Rn_





URI: [obographs:PropertyChainAxiom](https://github.com/geneontology/obographs/PropertyChainAxiom)






```{mermaid}
 classDiagram
    class PropertyChainAxiom
    click PropertyChainAxiom href "../PropertyChainAxiom"
      Axiom <|-- PropertyChainAxiom
        click Axiom href "../Axiom"
      
      PropertyChainAxiom : chainPredicateIds
        
      PropertyChainAxiom : meta
        
          
    
    
    PropertyChainAxiom --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      PropertyChainAxiom : predicateId
        
      
```





## Inheritance
* [Axiom](Axiom.md)
    * **PropertyChainAxiom**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [predicateId](predicateId.md) | 0..1 <br/> [String](String.md) |  | direct |
| [chainPredicateIds](chainPredicateIds.md) | * <br/> [String](String.md) | A list of identifiers of predicates that form the precedent clause of a prope... | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [Axiom](Axiom.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [propertyChainAxioms](propertyChainAxioms.md) | range | [PropertyChainAxiom](PropertyChainAxiom.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:PropertyChainAxiom |
| native | obographs:PropertyChainAxiom |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyChainAxiom
description: An axiom that represents an OWL property chain, e.g. R <- R1 o ... o
  Rn
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
slots:
- predicateId
- chainPredicateIds

```
</details>

### Induced

<details>
```yaml
name: PropertyChainAxiom
description: An axiom that represents an OWL property chain, e.g. R <- R1 o ... o
  Rn
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
attributes:
  predicateId:
    name: predicateId
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: predicateId
    owner: PropertyChainAxiom
    domain_of:
    - DomainRangeAxiom
    - PropertyChainAxiom
    range: string
  chainPredicateIds:
    name: chainPredicateIds
    description: A list of identifiers of predicates that form the precedent clause
      of a property chain rule
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: chainPredicateIds
    owner: PropertyChainAxiom
    domain_of:
    - PropertyChainAxiom
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
    owner: PropertyChainAxiom
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