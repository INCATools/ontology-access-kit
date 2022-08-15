# Class: PropertyValue


* __NOTE__: this is an abstract class and should not be instantiated directly



URI: [og:PropertyValue](https://github.com/geneontology/obographs/PropertyValue)




```{mermaid}
 classDiagram
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

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [pred](pred.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [val](val.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [xrefs](xrefs.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md)  |   |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:PropertyValue'] |
| native | ['og:PropertyValue'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyValue
from_schema: https://github.com/geneontology/obographs
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
from_schema: https://github.com/geneontology/obographs
rank: 1000
abstract: true
attributes:
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: pred
    owner: PropertyValue
    domain_of:
    - Edge
    - PropertyValue
    range: string
  val:
    name: val
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: val
    owner: PropertyValue
    domain_of:
    - PropertyValue
    range: string
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: xrefs
    owner: PropertyValue
    domain_of:
    - Meta
    - PropertyValue
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: PropertyValue
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta

```
</details>