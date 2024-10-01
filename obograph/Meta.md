

# Class: Meta


_A collection of annotations on an entity or ontology or edge or axiom. Metadata typically does not affect the logical interpretation of the container but provides useful information to humans or machines._





URI: [obographs:Meta](https://github.com/geneontology/obographs/Meta)






```{mermaid}
 classDiagram
    class Meta
    click Meta href "../Meta"
      Meta : basicPropertyValues
        
          
    
    
    Meta --> "*" BasicPropertyValue : basicPropertyValues
    click BasicPropertyValue href "../BasicPropertyValue"

        
      Meta : comments
        
      Meta : definition
        
          
    
    
    Meta --> "0..1" DefinitionPropertyValue : definition
    click DefinitionPropertyValue href "../DefinitionPropertyValue"

        
      Meta : deprecated
        
      Meta : subsets
        
      Meta : synonyms
        
          
    
    
    Meta --> "*" SynonymPropertyValue : synonyms
    click SynonymPropertyValue href "../SynonymPropertyValue"

        
      Meta : version
        
      Meta : xrefs
        
          
    
    
    Meta --> "*" XrefPropertyValue : xrefs
    click XrefPropertyValue href "../XrefPropertyValue"

        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subsets](subsets.md) | * <br/> [String](String.md) | A list of subsets to which this entity belongs | direct |
| [version](version.md) | 0..1 <br/> [String](String.md) |  | direct |
| [comments](comments.md) | * <br/> [String](String.md) | A list of comments about the entity | direct |
| [definition](definition.md) | 0..1 <br/> [DefinitionPropertyValue](DefinitionPropertyValue.md) | A definition of an entity | direct |
| [xrefs](xrefs.md) | * <br/> [XrefPropertyValue](XrefPropertyValue.md) | A list of cross references to other entities represented in other ontologies,... | direct |
| [synonyms](synonyms.md) | * <br/> [SynonymPropertyValue](SynonymPropertyValue.md) | A list of synonym property value assertions for an entity | direct |
| [basicPropertyValues](basicPropertyValues.md) | * <br/> [BasicPropertyValue](BasicPropertyValue.md) | A list of open-ended property values that does not correspond to those predef... | direct |
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
| [DisjointClassExpressionsAxiom](DisjointClassExpressionsAxiom.md) | [meta](meta.md) | range | [Meta](Meta.md) |
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
    range: XrefPropertyValue
    multivalued: true

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
slot_usage:
  xrefs:
    name: xrefs
    range: XrefPropertyValue
    multivalued: true
attributes:
  subsets:
    name: subsets
    description: A list of subsets to which this entity belongs
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: oio:inSubset
    alias: subsets
    owner: Meta
    domain_of:
    - Meta
    range: string
    multivalued: true
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
    alias: comments
    owner: Meta
    domain_of:
    - Meta
    range: string
    multivalued: true
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
    exact_mappings:
    - oio:hasDbXref
    close_mappings:
    - rdfs:seeAlso
    rank: 1000
    alias: xrefs
    owner: Meta
    domain_of:
    - Meta
    - PropertyValue
    range: XrefPropertyValue
    multivalued: true
  synonyms:
    name: synonyms
    description: A list of synonym property value assertions for an entity
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: synonyms
    owner: Meta
    domain_of:
    - Meta
    range: SynonymPropertyValue
    multivalued: true
  basicPropertyValues:
    name: basicPropertyValues
    description: A list of open-ended property values that does not correspond to
      those predefined in this standard, i.e xref, synonyms, definition
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: basicPropertyValues
    owner: Meta
    domain_of:
    - Meta
    range: BasicPropertyValue
    multivalued: true
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