# Class: Meta
_A collection of annotations on an entity or ontology or edge or axiom. Metadata typically does not affect the logical interpretation of the container but provides useful information to humans or machines._




URI: [obographs:Meta](https://github.com/geneontology/obographs/Meta)



```{mermaid}
 classDiagram
    class Meta
      Meta : basicPropertyValues
        
          Meta ..> BasicPropertyValue : basicPropertyValues
        
      Meta : comments
        
      Meta : definition
        
          Meta ..> DefinitionPropertyValue : definition
        
      Meta : deprecated
        
      Meta : subsets
        
      Meta : synonyms
        
          Meta ..> SynonymPropertyValue : synonyms
        
      Meta : version
        
      Meta : xrefs
        
          Meta ..> XrefPropertyValue : xrefs
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subsets](subsets.md) | 0..* <br/> [String](String.md) | A list of subsets to which this entity belongs | direct |
| [version](version.md) | 0..1 <br/> [String](String.md) |  | direct |
| [comments](comments.md) | 0..* <br/> [String](String.md) | A list of comments about the entity | direct |
| [definition](definition.md) | 0..1 <br/> [DefinitionPropertyValue](DefinitionPropertyValue.md) | A definition of an entity | direct |
| [xrefs](xrefs.md) | 0..* <br/> [XrefString](XrefString.md) | A list of cross references to other entities represented in other ontologies,... | direct |
| [synonyms](synonyms.md) | 0..* <br/> [SynonymPropertyValue](SynonymPropertyValue.md) | A list of synonym property value assertions for an entity | direct |
| [basicPropertyValues](basicPropertyValues.md) | 0..* <br/> [BasicPropertyValue](BasicPropertyValue.md) | A list of open-ended property values that does not correspond to those predef... | direct |
| [deprecated](deprecated.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [GraphDocument](GraphDocument.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [Graph](Graph.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [Node](Node.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [Edge](Edge.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [DefinitionPropertyValue](DefinitionPropertyValue.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [BasicPropertyValue](BasicPropertyValue.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [XrefPropertyValue](XrefPropertyValue.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [SynonymPropertyValue](SynonymPropertyValue.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [PropertyValue](PropertyValue.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [Axiom](Axiom.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [DomainRangeAxiom](DomainRangeAxiom.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [EquivalentNodesSet](EquivalentNodesSet.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | [meta](meta.md) | range | [Meta](Meta.md) |
| [PropertyChainAxiom](PropertyChainAxiom.md) | [meta](meta.md) | range | [Meta](Meta.md) |




## Aliases


* annotation collection



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:Meta |
| native | obographs:Meta |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Meta
description: A collection of annotations on an entity or ontology or edge or axiom.
  Metadata typically does not affect the logical interpretation of the container but
  provides useful information to humans or machines.
from_schema: https://github.com/geneontology/obographs
aliases:
- annotation collection
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
slot_usage:
  xrefs:
    name: xrefs
    multivalued: true
    domain_of:
    - Meta
    - PropertyValue
    range: XrefPropertyValue

```
</details>

### Induced

<details>
```yaml
name: Meta
description: A collection of annotations on an entity or ontology or edge or axiom.
  Metadata typically does not affect the logical interpretation of the container but
  provides useful information to humans or machines.
from_schema: https://github.com/geneontology/obographs
aliases:
- annotation collection
rank: 1000
slot_usage:
  xrefs:
    name: xrefs
    multivalued: true
    domain_of:
    - Meta
    - PropertyValue
    range: XrefPropertyValue
attributes:
  subsets:
    name: subsets
    description: A list of subsets to which this entity belongs
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: oio:inSubset
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
    slot_uri: owl:versionInfo
    alias: version
    owner: Meta
    domain_of:
    - Meta
    range: string
  comments:
    name: comments
    description: A list of comments about the entity
    comments:
    - for historic reasons obo format only supports a single comment per entity. This
      limitation is not carried over here, but users should be aware that multiple
      comments will not be supported in converting back to obo format.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdfs:comment
    multivalued: true
    alias: comments
    owner: Meta
    domain_of:
    - Meta
    range: string
  definition:
    name: definition
    description: A definition of an entity
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: IAO:0000115
    alias: definition
    owner: Meta
    domain_of:
    - Meta
    range: DefinitionPropertyValue
  xrefs:
    name: xrefs
    description: A list of cross references to other entities represented in other
      ontologies, vocabularies, databases, or websites. The semantics of xrefs are
      intentionally weak, and most closely align with rdfs:seeAlso
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: xrefs
    owner: Meta
    domain_of:
    - Meta
    - PropertyValue
    range: XrefPropertyValue
  synonyms:
    name: synonyms
    description: A list of synonym property value assertions for an entity
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
    description: A list of open-ended property values that does not correspond to
      those predefined in this standard, i.e xref, synonyms, definition
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
    slot_uri: owl:deprecated
    alias: deprecated
    owner: Meta
    domain_of:
    - Meta
    range: boolean

```
</details>