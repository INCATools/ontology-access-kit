# Class: SynonymPropertyValue
_A property value that represents an assertion about a synonym of an entity_




URI: [og:SynonymPropertyValue](https://github.com/geneontology/obographs/SynonymPropertyValue)



```{mermaid}
 classDiagram
    class SynonymPropertyValue
      PropertyValue <|-- SynonymPropertyValue
      
      SynonymPropertyValue : isExact
      SynonymPropertyValue : meta
      SynonymPropertyValue : pred
      SynonymPropertyValue : synonymType
      SynonymPropertyValue : val
      SynonymPropertyValue : xrefs
      
```





## Inheritance
* [PropertyValue](PropertyValue.md)
    * **SynonymPropertyValue**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [synonymType](synonymType.md) | 0..1 <br/> [SynonymTypeIdentifierString](SynonymTypeIdentifierString.md) | This standard follows oboInOwl in allowing an open ended list of synonym type... | direct |
| [isExact](isExact.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |  | direct |
| [pred](pred.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | the predicate of an edge | direct |
| [val](val.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The textual string representing the synonym | [PropertyValue](PropertyValue.md) |
| [xrefs](xrefs.md) | 0..* <br/> [XrefString](XrefString.md) | A list of cross references to other entities represented in other ontologies,... | [PropertyValue](PropertyValue.md) |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [PropertyValue](PropertyValue.md) |





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
| self | og:SynonymPropertyValue |
| native | og:SynonymPropertyValue |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SynonymPropertyValue
description: A property value that represents an assertion about a synonym of an entity
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
slots:
- synonymType
- isExact
- pred
slot_usage:
  pred:
    name: pred
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: ScopeEnum
  val:
    name: val
    description: The textual string representing the synonym.
    domain_of:
    - PropertyValue
    - PropertyValue
    role: synonym text

```
</details>

### Induced

<details>
```yaml
name: SynonymPropertyValue
description: A property value that represents an assertion about a synonym of an entity
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
slot_usage:
  pred:
    name: pred
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: ScopeEnum
  val:
    name: val
    description: The textual string representing the synonym.
    domain_of:
    - PropertyValue
    - PropertyValue
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
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: ScopeEnum
  val:
    name: val
    description: The textual string representing the synonym.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:object
    alias: val
    owner: SynonymPropertyValue
    domain_of:
    - PropertyValue
    - PropertyValue
    role: synonym text
    range: string
  xrefs:
    name: xrefs
    description: A list of cross references to other entities represented in other
      ontologies, vocabularies, databases, or websites. The semantics of xrefs are
      intentionally weak, and most closely align with rdfs:seeAlso
    from_schema: https://github.com/geneontology/obographs
    close_mappings:
    - rdfs:seeAlso
    rank: 1000
    multivalued: true
    alias: xrefs
    owner: SynonymPropertyValue
    domain_of:
    - Meta
    - PropertyValue
    range: XrefString
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

```
</details>