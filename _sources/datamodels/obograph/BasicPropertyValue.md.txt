# Class: BasicPropertyValue
_A property value that represents an assertion about an entity that is not a definition, synonym, or xref_




URI: [og:BasicPropertyValue](https://github.com/geneontology/obographs/BasicPropertyValue)



```{mermaid}
 classDiagram
    class BasicPropertyValue
      PropertyValue <|-- BasicPropertyValue
      
      BasicPropertyValue : meta
      BasicPropertyValue : pred
      BasicPropertyValue : val
      BasicPropertyValue : xrefs
      
```





## Inheritance
* [PropertyValue](PropertyValue.md)
    * **BasicPropertyValue**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [pred](pred.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | the predicate of an edge | [PropertyValue](PropertyValue.md) |
| [val](val.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | the value of a property | [PropertyValue](PropertyValue.md) |
| [xrefs](xrefs.md) | 0..* <br/> [XrefString](XrefString.md) | A list of cross references to other entities represented in other ontologies,... | [PropertyValue](PropertyValue.md) |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [PropertyValue](PropertyValue.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Meta](Meta.md) | [basicPropertyValues](basicPropertyValues.md) | range | [BasicPropertyValue](BasicPropertyValue.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | og:BasicPropertyValue |
| native | og:BasicPropertyValue |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: BasicPropertyValue
description: A property value that represents an assertion about an entity that is
  not a definition, synonym, or xref
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue

```
</details>

### Induced

<details>
```yaml
name: BasicPropertyValue
description: A property value that represents an assertion about an entity that is
  not a definition, synonym, or xref
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
attributes:
  pred:
    name: pred
    description: the predicate of an edge
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:predicate
    alias: pred
    owner: BasicPropertyValue
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: string
  val:
    name: val
    description: the value of a property
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:object
    alias: val
    owner: BasicPropertyValue
    domain_of:
    - PropertyValue
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
    owner: BasicPropertyValue
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
    owner: BasicPropertyValue
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