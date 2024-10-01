

# Class: PropertyValue


_A generic grouping for the different kinds of key-value associations on object. Minimally, a property value has a predicate and a value. It can also have a list of xrefs indicating provenance, as well as a metadata object._




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [obographs:PropertyValue](https://github.com/geneontology/obographs/PropertyValue)






```{mermaid}
 classDiagram
    class PropertyValue
    click PropertyValue href "../PropertyValue"
      PropertyValue <|-- DefinitionPropertyValue
        click DefinitionPropertyValue href "../DefinitionPropertyValue"
      PropertyValue <|-- BasicPropertyValue
        click BasicPropertyValue href "../BasicPropertyValue"
      PropertyValue <|-- XrefPropertyValue
        click XrefPropertyValue href "../XrefPropertyValue"
      PropertyValue <|-- SynonymPropertyValue
        click SynonymPropertyValue href "../SynonymPropertyValue"
      
      PropertyValue : lang
        
      PropertyValue : meta
        
          
    
    
    PropertyValue --> "0..1" Meta : meta
    click Meta href "../Meta"

        
      PropertyValue : pred
        
      PropertyValue : val
        
      PropertyValue : valType
        
      PropertyValue : xrefs
        
      
```





## Inheritance
* **PropertyValue**
    * [DefinitionPropertyValue](DefinitionPropertyValue.md)
    * [BasicPropertyValue](BasicPropertyValue.md)
    * [XrefPropertyValue](XrefPropertyValue.md)
    * [SynonymPropertyValue](SynonymPropertyValue.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [pred](pred.md) | 0..1 <br/> [String](String.md) | the predicate of an edge | direct |
| [val](val.md) | 0..1 <br/> [String](String.md) | the value of a property | direct |
| [xrefs](xrefs.md) | * <br/> [XrefString](XrefString.md) | A list of cross references to other entities represented in other ontologies,... | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | direct |
| [valType](valType.md) | 0..1 <br/> [String](String.md) | the datatype of a property value | direct |
| [lang](lang.md) | 0..1 <br/> [String](String.md) | the language of a property value | direct |







## Aliases


* annotation



## Comments

* Any PropertyValue can have a meta object, which can itself have basicPropertyValues, meaning that like the OWL annotation model, axiom annotations can be nested to arbitrary levels.

## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | obographs:PropertyValue |
| native | obographs:PropertyValue |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyValue
description: A generic grouping for the different kinds of key-value associations
  on object. Minimally, a property value has a predicate and a value. It can also
  have a list of xrefs indicating provenance, as well as a metadata object.
comments:
- Any PropertyValue can have a meta object, which can itself have basicPropertyValues,
  meaning that like the OWL annotation model, axiom annotations can be nested to arbitrary
  levels.
from_schema: https://github.com/geneontology/obographs
aliases:
- annotation
abstract: true
slots:
- pred
- val
- xrefs
- meta
- valType
- lang

```
</details>

### Induced

<details>
```yaml
name: PropertyValue
description: A generic grouping for the different kinds of key-value associations
  on object. Minimally, a property value has a predicate and a value. It can also
  have a list of xrefs indicating provenance, as well as a metadata object.
comments:
- Any PropertyValue can have a meta object, which can itself have basicPropertyValues,
  meaning that like the OWL annotation model, axiom annotations can be nested to arbitrary
  levels.
from_schema: https://github.com/geneontology/obographs
aliases:
- annotation
abstract: true
attributes:
  pred:
    name: pred
    description: the predicate of an edge
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    slot_uri: rdf:predicate
    alias: pred
    owner: PropertyValue
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - SynonymTypeDefinition
    range: string
  val:
    name: val
    description: the value of a property
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - value
    rank: 1000
    slot_uri: rdf:object
    alias: val
    owner: PropertyValue
    domain_of:
    - PropertyValue
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
    owner: PropertyValue
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
    owner: PropertyValue
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
    owner: PropertyValue
    domain_of:
    - PropertyValue
    range: string
  lang:
    name: lang
    description: the language of a property value
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: lang
    owner: PropertyValue
    domain_of:
    - PropertyValue
    range: string

```
</details>