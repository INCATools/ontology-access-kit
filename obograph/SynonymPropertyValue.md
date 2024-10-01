

# Class: SynonymPropertyValue


_A property value that represents an assertion about a synonym of an entity_





URI: [obographs:SynonymPropertyValue](https://github.com/geneontology/obographs/SynonymPropertyValue)






```{mermaid}
 classDiagram
    class SynonymPropertyValue
    click SynonymPropertyValue href "../SynonymPropertyValue"
      PropertyValue <|-- SynonymPropertyValue
        click PropertyValue href "../PropertyValue"
      
      SynonymPropertyValue : isExact
        
      SynonymPropertyValue : lang
        
      SynonymPropertyValue : meta
        
          
    
    
    SynonymPropertyValue --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      SynonymPropertyValue : pred
        
          
    
    
    SynonymPropertyValue --> "0..1" ScopeEnum : pred
    click ScopeEnum href "../ScopeEnum"

        
      SynonymPropertyValue : synonymType
        
      SynonymPropertyValue : val
        
      SynonymPropertyValue : valType
        
      SynonymPropertyValue : xrefs
        
      
```





## Inheritance
* [PropertyValue](PropertyValue.md)
    * **SynonymPropertyValue**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [synonymType](synonymType.md) | 0..1 <br/> [SynonymTypeIdentifierString](SynonymTypeIdentifierString.md) | This standard follows oboInOwl in allowing an open ended list of synonym type... | direct |
| [isExact](isExact.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [pred](pred.md) | 0..1 <br/> [ScopeEnum](ScopeEnum.md) | the predicate of an edge | direct |
| [val](val.md) | 0..1 <br/> [String](String.md) | The textual string representing the synonym | [PropertyValue](PropertyValue.md) |
| [xrefs](xrefs.md) | * <br/> [XrefString](XrefString.md) | A list of cross references to other entities represented in other ontologies,... | [PropertyValue](PropertyValue.md) |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [PropertyValue](PropertyValue.md) |
| [valType](valType.md) | 0..1 <br/> [String](String.md) | the datatype of a property value | [PropertyValue](PropertyValue.md) |
| [lang](lang.md) | 0..1 <br/> [String](String.md) | the language of a property value | [PropertyValue](PropertyValue.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Meta](Meta.md) | [synonyms](synonyms.md) | range | [SynonymPropertyValue](SynonymPropertyValue.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:SynonymPropertyValue |
| native | obographs:SynonymPropertyValue |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SynonymPropertyValue
description: A property value that represents an assertion about a synonym of an entity
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
slots:
- synonymType
- isExact
- pred
slot_usage:
  pred:
    name: pred
    range: ScopeEnum
  val:
    name: val
    description: The textual string representing the synonym.
    role: synonym text

```
</details>

### Induced

<details>
```yaml
name: SynonymPropertyValue
description: A property value that represents an assertion about a synonym of an entity
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
slot_usage:
  pred:
    name: pred
    range: ScopeEnum
  val:
    name: val
    description: The textual string representing the synonym.
    role: synonym text
attributes:
  synonymType:
    name: synonymType
    description: This standard follows oboInOwl in allowing an open ended list of
      synonym types
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: synonymType
    owner: SynonymPropertyValue
    domain_of:
    - SynonymPropertyValue
    range: SynonymTypeIdentifierString
  isExact:
    name: isExact
    deprecated: use synonymType instead
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: isExact
    owner: SynonymPropertyValue
    domain_of:
    - SynonymPropertyValue
    range: boolean
  pred:
    name: pred
    description: the predicate of an edge
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:predicate
    alias: pred
    owner: SynonymPropertyValue
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - SynonymTypeDefinition
    range: ScopeEnum
  val:
    name: val
    description: The textual string representing the synonym.
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - value
    rank: 1000
    slot_uri: rdf:object
    alias: val
    owner: SynonymPropertyValue
    domain_of:
    - PropertyValue
    role: synonym text
    range: string
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
    owner: SynonymPropertyValue
    domain_of:
    - Meta
    - PropertyValue
    range: XrefString
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
    owner: SynonymPropertyValue
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - Edge
    - PropertyValue
    - Axiom
    range: Meta
  valType:
    name: valType
    description: the datatype of a property value
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - value type
    - datatype
    rank: 1000
    alias: valType
    owner: SynonymPropertyValue
    domain_of:
    - PropertyValue
    range: string
  lang:
    name: lang
    description: the language of a property value
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: lang
    owner: SynonymPropertyValue
    domain_of:
    - PropertyValue
    range: string

```
</details>