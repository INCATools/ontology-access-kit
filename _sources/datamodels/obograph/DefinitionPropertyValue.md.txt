# Class: DefinitionPropertyValue
_A property value that represents an assertion about the textual definition of an entity_




URI: [og:DefinitionPropertyValue](https://github.com/geneontology/obographs/DefinitionPropertyValue)



```{mermaid}
 classDiagram
    class DefinitionPropertyValue
      PropertyValue <|-- DefinitionPropertyValue
      
      DefinitionPropertyValue : meta
      DefinitionPropertyValue : pred
      DefinitionPropertyValue : val
      DefinitionPropertyValue : xrefs
      
```





## Inheritance
* [PropertyValue](PropertyValue.md)
    * **DefinitionPropertyValue**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [pred](pred.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | the predicate of an edge | [PropertyValue](PropertyValue.md) |
| [val](val.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | The textual string representing the definition | [PropertyValue](PropertyValue.md) |
| [xrefs](xrefs.md) | 0..* <br/> [XrefString](XrefString.md) | A list of identifiers that support the definition | [PropertyValue](PropertyValue.md) |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [PropertyValue](PropertyValue.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Meta](Meta.md) | [definition](definition.md) | range | [DefinitionPropertyValue](DefinitionPropertyValue.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | og:DefinitionPropertyValue |
| native | og:DefinitionPropertyValue |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DefinitionPropertyValue
description: A property value that represents an assertion about the textual definition
  of an entity
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
slot_usage:
  val:
    name: val
    description: The textual string representing the definition.
    domain_of:
    - PropertyValue
    - PropertyValue
    role: definition text
  xrefs:
    name: xrefs
    description: A list of identifiers that support the definition. The semantics
      are intentionally broad, and these identifiers might represent individual agents
      that contributed to the text of the definition, external publications, websites,
      or links to supporting information, or external vocabulary entities that played
      a contributing role in the definition.
    domain_of:
    - Meta
    - PropertyValue
    - Meta
    - PropertyValue
    role: supporting identifiers

```
</details>

### Induced

<details>
```yaml
name: DefinitionPropertyValue
description: A property value that represents an assertion about the textual definition
  of an entity
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
slot_usage:
  val:
    name: val
    description: The textual string representing the definition.
    domain_of:
    - PropertyValue
    - PropertyValue
    role: definition text
  xrefs:
    name: xrefs
    description: A list of identifiers that support the definition. The semantics
      are intentionally broad, and these identifiers might represent individual agents
      that contributed to the text of the definition, external publications, websites,
      or links to supporting information, or external vocabulary entities that played
      a contributing role in the definition.
    domain_of:
    - Meta
    - PropertyValue
    - Meta
    - PropertyValue
    role: supporting identifiers
attributes:
  pred:
    name: pred
    description: the predicate of an edge
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:predicate
    alias: pred
    owner: DefinitionPropertyValue
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: string
  val:
    name: val
    description: The textual string representing the definition.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:object
    alias: val
    owner: DefinitionPropertyValue
    domain_of:
    - PropertyValue
    - PropertyValue
    role: definition text
    range: string
  xrefs:
    name: xrefs
    description: A list of identifiers that support the definition. The semantics
      are intentionally broad, and these identifiers might represent individual agents
      that contributed to the text of the definition, external publications, websites,
      or links to supporting information, or external vocabulary entities that played
      a contributing role in the definition.
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: xrefs
    owner: DefinitionPropertyValue
    domain_of:
    - Meta
    - PropertyValue
    - Meta
    - PropertyValue
    role: supporting identifiers
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
    owner: DefinitionPropertyValue
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