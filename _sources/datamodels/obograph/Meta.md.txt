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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [subsets](subsets.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [version](version.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [comments](comments.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [definition](definition.md) | [DefinitionPropertyValue](DefinitionPropertyValue.md) | 0..1 | None  | . |
| [xrefs](xrefs.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [synonyms](synonyms.md) | [SynonymPropertyValue](SynonymPropertyValue.md) | 0..* | None  | . |
| [basicPropertyValues](basicPropertyValues.md) | [BasicPropertyValue](BasicPropertyValue.md) | 0..* | None  | . |
| [deprecated](deprecated.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |


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
attributes:
  subsets:
    name: subsets
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: subsets
    owner: Meta
    range: string
  version:
    name: version
    from_schema: https://github.com/geneontology/obographs
    alias: version
    owner: Meta
    range: string
  comments:
    name: comments
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: comments
    owner: Meta
    range: string
  definition:
    name: definition
    from_schema: https://github.com/geneontology/obographs
    alias: definition
    owner: Meta
    range: DefinitionPropertyValue
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: xrefs
    owner: Meta
    range: string
  synonyms:
    name: synonyms
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: synonyms
    owner: Meta
    range: SynonymPropertyValue
  basicPropertyValues:
    name: basicPropertyValues
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: basicPropertyValues
    owner: Meta
    range: BasicPropertyValue
  deprecated:
    name: deprecated
    from_schema: https://github.com/geneontology/obographs
    alias: deprecated
    owner: Meta
    range: boolean

```
</details>