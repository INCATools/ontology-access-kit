# Class: Meta




URI: [og:Meta](https://github.com/geneontology/obographs/Meta)




```{mermaid}
 classDiagram
    class Meta
      Meta : basicPropertyValues
      Meta : comments
      Meta : definition
      Meta : deprecated
      Meta : subsets
      Meta : synonyms
      Meta : version
      Meta : xrefs
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [subsets](subsets.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [version](version.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [comments](comments.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [definition](definition.md) | 0..1 <br/> [DefinitionPropertyValue](DefinitionPropertyValue.md)  |   |
| [xrefs](xrefs.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [synonyms](synonyms.md) | 0..* <br/> [SynonymPropertyValue](SynonymPropertyValue.md)  |   |
| [basicPropertyValues](basicPropertyValues.md) | 0..* <br/> [BasicPropertyValue](BasicPropertyValue.md)  |   |
| [deprecated](deprecated.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean)  |   |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GraphDocument](GraphDocument.md) | [meta](meta.md) | range | Meta |
| [Graph](Graph.md) | [meta](meta.md) | range | Meta |
| [Node](Node.md) | [meta](meta.md) | range | Meta |
| [DefinitionPropertyValue](DefinitionPropertyValue.md) | [meta](meta.md) | range | Meta |
| [BasicPropertyValue](BasicPropertyValue.md) | [meta](meta.md) | range | Meta |
| [XrefPropertyValue](XrefPropertyValue.md) | [meta](meta.md) | range | Meta |
| [SynonymPropertyValue](SynonymPropertyValue.md) | [meta](meta.md) | range | Meta |
| [PropertyValue](PropertyValue.md) | [meta](meta.md) | range | Meta |
| [Axiom](Axiom.md) | [meta](meta.md) | range | Meta |
| [DomainRangeAxiom](DomainRangeAxiom.md) | [meta](meta.md) | range | Meta |
| [EquivalentNodesSet](EquivalentNodesSet.md) | [meta](meta.md) | range | Meta |
| [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | [meta](meta.md) | range | Meta |
| [PropertyChainAxiom](PropertyChainAxiom.md) | [meta](meta.md) | range | Meta |



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:Meta'] |
| native | ['og:Meta'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Meta
from_schema: https://github.com/geneontology/obographs
rank: 1000
slots:
- subsets
- version
- comments
- definition
- xrefs
- synonyms
- basicPropertyValues
- deprecated

```
</details>

### Induced

<details>
```yaml
name: Meta
from_schema: https://github.com/geneontology/obographs
rank: 1000
attributes:
  subsets:
    name: subsets
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: subsets
    owner: Meta
    domain_of:
    - Meta
    range: string
  version:
    name: version
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: version
    owner: Meta
    domain_of:
    - Meta
    range: string
  comments:
    name: comments
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: comments
    owner: Meta
    domain_of:
    - Meta
    range: string
  definition:
    name: definition
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: definition
    owner: Meta
    domain_of:
    - Meta
    range: DefinitionPropertyValue
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: xrefs
    owner: Meta
    domain_of:
    - Meta
    - PropertyValue
    range: string
  synonyms:
    name: synonyms
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: synonyms
    owner: Meta
    domain_of:
    - Meta
    range: SynonymPropertyValue
  basicPropertyValues:
    name: basicPropertyValues
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: basicPropertyValues
    owner: Meta
    domain_of:
    - Meta
    range: BasicPropertyValue
  deprecated:
    name: deprecated
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: deprecated
    owner: Meta
    domain_of:
    - Meta
    range: boolean

```
</details>