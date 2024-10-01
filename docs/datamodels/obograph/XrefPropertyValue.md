

# Class: XrefPropertyValue


_A property value that represents an assertion about an external reference to an entity_





URI: [obographs:XrefPropertyValue](https://github.com/geneontology/obographs/XrefPropertyValue)






```{mermaid}
 classDiagram
    class XrefPropertyValue
    click XrefPropertyValue href "../XrefPropertyValue"
      PropertyValue <|-- XrefPropertyValue
        click PropertyValue href "../PropertyValue"
      
      XrefPropertyValue : lang
        
      XrefPropertyValue : meta
        
          
    
    
    XrefPropertyValue --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      XrefPropertyValue : pred
        
      XrefPropertyValue : val
        
      XrefPropertyValue : valType
        
      XrefPropertyValue : xrefs
        
      
```





## Inheritance
* [PropertyValue](PropertyValue.md)
    * **XrefPropertyValue**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [pred](pred.md) | 0..1 <br/> [String](String.md) | the predicate of an edge | [PropertyValue](PropertyValue.md) |
| [val](val.md) | 0..1 <br/> [String](String.md) | The textual representation of the external reference, e | [PropertyValue](PropertyValue.md) |
| [xrefs](xrefs.md) | * <br/> [XrefString](XrefString.md) | A list of cross references to other entities represented in other ontologies,... | [PropertyValue](PropertyValue.md) |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [PropertyValue](PropertyValue.md) |
| [valType](valType.md) | 0..1 <br/> [String](String.md) | the datatype of a property value | [PropertyValue](PropertyValue.md) |
| [lang](lang.md) | 0..1 <br/> [String](String.md) | the language of a property value | [PropertyValue](PropertyValue.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Meta](Meta.md) | [xrefs](xrefs.md) | range | [XrefPropertyValue](XrefPropertyValue.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:XrefPropertyValue |
| native | obographs:XrefPropertyValue |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: XrefPropertyValue
description: A property value that represents an assertion about an external reference
  to an entity
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
slot_usage:
  val:
    name: val
    description: The textual representation of the external reference, e.g. "PMID:12345"
    role: xref

```
</details>

### Induced

<details>
```yaml
name: XrefPropertyValue
description: A property value that represents an assertion about an external reference
  to an entity
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
slot_usage:
  val:
    name: val
    description: The textual representation of the external reference, e.g. "PMID:12345"
    role: xref
attributes:
  pred:
    name: pred
    description: the predicate of an edge
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:predicate
    alias: pred
    owner: XrefPropertyValue
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - SynonymTypeDefinition
    range: string
  val:
    name: val
    description: The textual representation of the external reference, e.g. "PMID:12345"
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - value
    rank: 1000
    slot_uri: rdf:object
    alias: val
    owner: XrefPropertyValue
    domain_of:
    - PropertyValue
    role: xref
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
    owner: XrefPropertyValue
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
    owner: XrefPropertyValue
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
    owner: XrefPropertyValue
    domain_of:
    - PropertyValue
    range: string
  lang:
    name: lang
    description: the language of a property value
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: lang
    owner: XrefPropertyValue
    domain_of:
    - PropertyValue
    range: string

```
</details>