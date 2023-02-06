# Class: PropertyValue
_A generic grouping for the different kinds of key-value associations on object. Minimally, a property value has a predicate and a value. It can also have a list of xrefs indicating provenance, as well as a metadata object._



* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [og:PropertyValue](https://github.com/geneontology/obographs/PropertyValue)



```{mermaid}
 classDiagram
    class PropertyValue
      PropertyValue <|-- DefinitionPropertyValue
      PropertyValue <|-- BasicPropertyValue
      PropertyValue <|-- XrefPropertyValue
      PropertyValue <|-- SynonymPropertyValue
      
      PropertyValue : meta
      PropertyValue : pred
      PropertyValue : val
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
| [pred](pred.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | the predicate of an edge | direct |
| [val](val.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) | the value of a property | direct |
| [xrefs](xrefs.md) | 0..* <br/> [XrefString](XrefString.md) | A list of cross references to other entities represented in other ontologies,... | direct |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md) | A collection of metadata about either an ontology (graph), an entity, or an a... | direct |







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
| self | og:PropertyValue |
| native | og:PropertyValue |





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
rank: 1000
abstract: true
slots:
- pred
- val
- xrefs
- meta

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
rank: 1000
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
    range: string
  val:
    name: val
    description: the value of a property
    from_schema: https://github.com/geneontology/obographs
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
    close_mappings:
    - rdfs:seeAlso
    rank: 1000
    multivalued: true
    alias: xrefs
    owner: PropertyValue
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
    owner: PropertyValue
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