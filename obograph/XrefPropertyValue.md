# Class: XrefPropertyValue
_A property value that represents an assertion about an external reference to an entity_




URI: [og:XrefPropertyValue](https://github.com/geneontology/obographs/XrefPropertyValue)



```{mermaid}
 classDiagram
    class XrefPropertyValue
      PropertyValue <|-- XrefPropertyValue
      
      XrefPropertyValue : meta
      XrefPropertyValue : pred
      XrefPropertyValue : val
      XrefPropertyValue : xrefs
      
```





## Inheritance
* [PropertyValue](PropertyValue.md)
    * **XrefPropertyValue**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [pred](pred.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | the predicate of an edge | [PropertyValue](PropertyValue.md) |
| [val](val.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The textual representation of the external reference, e | [PropertyValue](PropertyValue.md) |
| [xrefs](xrefs.md) | 0..* <br/> [XrefString](XrefString.md) | A list of cross references to other entities represented in other ontologies,... | [PropertyValue](PropertyValue.md) |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [PropertyValue](PropertyValue.md) |





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
| self | og:XrefPropertyValue |
| native | og:XrefPropertyValue |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: XrefPropertyValue
description: A property value that represents an assertion about an external reference
  to an entity
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
slot_usage:
  val:
    name: val
    description: The textual representation of the external reference, e.g. "PMID:12345"
    domain_of:
    - PropertyValue
    - PropertyValue
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
rank: 1000
is_a: PropertyValue
slot_usage:
  val:
    name: val
    description: The textual representation of the external reference, e.g. "PMID:12345"
    domain_of:
    - PropertyValue
    - PropertyValue
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
    range: string
  val:
    name: val
    description: The textual representation of the external reference, e.g. "PMID:12345"
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:object
    alias: val
    owner: XrefPropertyValue
    domain_of:
    - PropertyValue
    - PropertyValue
    role: xref
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
    owner: XrefPropertyValue
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
    owner: XrefPropertyValue
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