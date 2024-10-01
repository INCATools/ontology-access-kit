

# Class: Axiom


_A generic grouping for any OWL axiom or group of axioms that is not captured by existing constructs in this standard._

__




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [owl:Axiom](http://www.w3.org/2002/07/owl#Axiom)






```{mermaid}
 classDiagram
    class Axiom
    click Axiom href "../Axiom"
      Axiom <|-- DomainRangeAxiom
        click DomainRangeAxiom href "../DomainRangeAxiom"
      Axiom <|-- EquivalentNodesSet
        click EquivalentNodesSet href "../EquivalentNodesSet"
      Axiom <|-- LogicalDefinitionAxiom
        click LogicalDefinitionAxiom href "../LogicalDefinitionAxiom"
      Axiom <|-- DisjointClassExpressionsAxiom
        click DisjointClassExpressionsAxiom href "../DisjointClassExpressionsAxiom"
      Axiom <|-- PropertyChainAxiom
        click PropertyChainAxiom href "../PropertyChainAxiom"
      
      Axiom : meta
        
          
    
    
    Axiom --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      
```





## Inheritance
* **Axiom**
    * [DomainRangeAxiom](DomainRangeAxiom.md)
    * [EquivalentNodesSet](EquivalentNodesSet.md)
    * [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md)
    * [DisjointClassExpressionsAxiom](DisjointClassExpressionsAxiom.md)
    * [PropertyChainAxiom](PropertyChainAxiom.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:Axiom |
| native | obographs:Axiom |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Axiom
description: 'A generic grouping for any OWL axiom or group of axioms that is not
  captured by existing constructs in this standard.

  '
from_schema: https://github.com/geneontology/obographs
abstract: true
slots:
- meta
class_uri: owl:Axiom

```
</details>

### Induced

<details>
```yaml
name: Axiom
description: 'A generic grouping for any OWL axiom or group of axioms that is not
  captured by existing constructs in this standard.

  '
from_schema: https://github.com/geneontology/obographs
abstract: true
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
    owner: Axiom
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - Edge
    - PropertyValue
    - Axiom
    range: Meta
class_uri: owl:Axiom

```
</details>