

# Class: DomainRangeAxiom


_This groups potentially multiple axioms that constrain the usage of a property depending on some combination of domain and range._





URI: [obographs:DomainRangeAxiom](https://github.com/geneontology/obographs/DomainRangeAxiom)






```{mermaid}
 classDiagram
    class DomainRangeAxiom
    click DomainRangeAxiom href "../DomainRangeAxiom"
      Axiom <|-- DomainRangeAxiom
        click Axiom href "../Axiom"
      
      DomainRangeAxiom : allValuesFromEdges
        
          
    
    
    DomainRangeAxiom --> "*" Edge : allValuesFromEdges
    click Edge href "../Edge"

        
      DomainRangeAxiom : domainClassIds
        
      DomainRangeAxiom : meta
        
          
    
    
    DomainRangeAxiom --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      DomainRangeAxiom : predicateId
        
      DomainRangeAxiom : rangeClassIds
        
      
```





## Inheritance
* [Axiom](Axiom.md)
    * **DomainRangeAxiom**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [predicateId](predicateId.md) | 0..1 <br/> [String](String.md) |  | direct |
| [domainClassIds](domainClassIds.md) | * <br/> [String](String.md) |  | direct |
| [rangeClassIds](rangeClassIds.md) | * <br/> [String](String.md) |  | direct |
| [allValuesFromEdges](allValuesFromEdges.md) | * <br/> [Edge](Edge.md) | A list of edges that represent subclasses of universal restrictions | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [Axiom](Axiom.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [domainRangeAxioms](domainRangeAxioms.md) | range | [DomainRangeAxiom](DomainRangeAxiom.md) |






## Comments

* When converting from OWL, an OWL domain axiom may be translated to a DomainRangeAxiom with a domainClassIds, and no rangeClassIds. An OWL range axiom may be translated to a DomainRangeAxiom with a rangeClassIds, and no domainClassIds. But translations may merge these, but only when semantically valid.

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:DomainRangeAxiom |
| native | obographs:DomainRangeAxiom |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DomainRangeAxiom
description: This groups potentially multiple axioms that constrain the usage of a
  property depending on some combination of domain and range.
comments:
- When converting from OWL, an OWL domain axiom may be translated to a DomainRangeAxiom
  with a domainClassIds, and no rangeClassIds. An OWL range axiom may be translated
  to a DomainRangeAxiom with a rangeClassIds, and no domainClassIds. But translations
  may merge these, but only when semantically valid.
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
slots:
- predicateId
- domainClassIds
- rangeClassIds
- allValuesFromEdges

```
</details>

### Induced

<details>
```yaml
name: DomainRangeAxiom
description: This groups potentially multiple axioms that constrain the usage of a
  property depending on some combination of domain and range.
comments:
- When converting from OWL, an OWL domain axiom may be translated to a DomainRangeAxiom
  with a domainClassIds, and no rangeClassIds. An OWL range axiom may be translated
  to a DomainRangeAxiom with a rangeClassIds, and no domainClassIds. But translations
  may merge these, but only when semantically valid.
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
attributes:
  predicateId:
    name: predicateId
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: predicateId
    owner: DomainRangeAxiom
    domain_of:
    - DomainRangeAxiom
    - PropertyChainAxiom
    range: string
  domainClassIds:
    name: domainClassIds
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: domainClassIds
    owner: DomainRangeAxiom
    domain_of:
    - DomainRangeAxiom
    range: string
    multivalued: true
  rangeClassIds:
    name: rangeClassIds
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: rangeClassIds
    owner: DomainRangeAxiom
    domain_of:
    - DomainRangeAxiom
    range: string
    multivalued: true
  allValuesFromEdges:
    name: allValuesFromEdges
    description: A list of edges that represent subclasses of universal restrictions
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: allValuesFromEdges
    owner: DomainRangeAxiom
    domain_of:
    - Graph
    - DomainRangeAxiom
    range: Edge
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
    owner: DomainRangeAxiom
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