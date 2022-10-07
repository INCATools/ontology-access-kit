# Class: PropertyChainAxiom




URI: [og:PropertyChainAxiom](https://github.com/geneontology/obographs/PropertyChainAxiom)




```{mermaid}
 classDiagram
    class PropertyChainAxiom
      Axiom <|-- PropertyChainAxiom
      
      PropertyChainAxiom : chainPredicateIds
      PropertyChainAxiom : meta
      PropertyChainAxiom : predicateId
      
```





## Inheritance
* [Axiom](Axiom.md)
    * **PropertyChainAxiom**



## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [predicateId](predicateId.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [chainPredicateIds](chainPredicateIds.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md)  |   |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [propertyChainAxioms](propertyChainAxioms.md) | range | PropertyChainAxiom |



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:PropertyChainAxiom'] |
| native | ['og:PropertyChainAxiom'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyChainAxiom
from_schema: https://github.com/geneontology/obographs
rank: 1000
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
from_schema: https://github.com/geneontology/obographs
rank: 1000
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
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: chainPredicateIds
    owner: PropertyChainAxiom
    domain_of:
    - PropertyChainAxiom
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: PropertyChainAxiom
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta

```
</details>