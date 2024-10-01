

# Class: DefinitionPropertyValue


_A property value that represents an assertion about the textual definition of an entity_





URI: [obographs:DefinitionPropertyValue](https://github.com/geneontology/obographs/DefinitionPropertyValue)






```{mermaid}
 classDiagram
    class DefinitionPropertyValue
    click DefinitionPropertyValue href "../DefinitionPropertyValue"
      PropertyValue <|-- DefinitionPropertyValue
        click PropertyValue href "../PropertyValue"
      
      DefinitionPropertyValue : lang
        
      DefinitionPropertyValue : meta
        
          
    
    
    DefinitionPropertyValue --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      DefinitionPropertyValue : pred
        
      DefinitionPropertyValue : val
        
      DefinitionPropertyValue : valType
        
      DefinitionPropertyValue : xrefs
        
      
```





## Inheritance
* [PropertyValue](PropertyValue.md)
    * **DefinitionPropertyValue**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [pred](pred.md) | 0..1 <br/> [String](String.md) | the predicate of an edge | [PropertyValue](PropertyValue.md) |
| [val](val.md) | 0..1 <br/> [String](String.md) | The textual string representing the definition | [PropertyValue](PropertyValue.md) |
| [xrefs](xrefs.md) | * <br/> [XrefString](XrefString.md) | A list of identifiers that support the definition | [PropertyValue](PropertyValue.md) |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | [PropertyValue](PropertyValue.md) |
| [valType](valType.md) | 0..1 <br/> [String](String.md) | the datatype of a property value | [PropertyValue](PropertyValue.md) |
| [lang](lang.md) | 0..1 <br/> [String](String.md) | the language of a property value | [PropertyValue](PropertyValue.md) |





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
| self | obographs:DefinitionPropertyValue |
| native | obographs:DefinitionPropertyValue |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DefinitionPropertyValue
description: A property value that represents an assertion about the textual definition
  of an entity
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
slot_usage:
  val:
    name: val
    description: The textual string representing the definition.
    role: definition text
  xrefs:
    name: xrefs
    description: A list of identifiers that support the definition. The semantics
      are intentionally broad, and these identifiers might represent individual agents
      that contributed to the text of the definition, external publications, websites,
      or links to supporting information, or external vocabulary entities that played
      a contributing role in the definition.
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
is_a: PropertyValue
slot_usage:
  val:
    name: val
    description: The textual string representing the definition.
    role: definition text
  xrefs:
    name: xrefs
    description: A list of identifiers that support the definition. The semantics
      are intentionally broad, and these identifiers might represent individual agents
      that contributed to the text of the definition, external publications, websites,
      or links to supporting information, or external vocabulary entities that played
      a contributing role in the definition.
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
    - SynonymTypeDefinition
    range: string
  val:
    name: val
    description: The textual string representing the definition.
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - value
    rank: 1000
    slot_uri: rdf:object
    alias: val
    owner: DefinitionPropertyValue
    domain_of:
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
    exact_mappings:
    - oio:hasDbXref
    close_mappings:
    - rdfs:seeAlso
    rank: 1000
    alias: xrefs
    owner: DefinitionPropertyValue
    domain_of:
    - Meta
    - PropertyValue
    role: supporting identifiers
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
    owner: DefinitionPropertyValue
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
    owner: DefinitionPropertyValue
    domain_of:
    - PropertyValue
    range: string
  lang:
    name: lang
    description: the language of a property value
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: lang
    owner: DefinitionPropertyValue
    domain_of:
    - PropertyValue
    range: string

```
</details>