# Class: XrefPropertyValue




URI: [og:XrefPropertyValue](https://github.com/geneontology/obographs/XrefPropertyValue)




```{mermaid}
 classDiagram
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
| self | ['og:XrefPropertyValue'] |
| native | ['og:XrefPropertyValue'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: XrefPropertyValue
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue

```
</details>

### Induced

<details>
```yaml
name: XrefPropertyValue
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
attributes:
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: pred
    owner: XrefPropertyValue
    domain_of:
    - Edge
    - PropertyValue
    range: string
  val:
    name: val
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: val
    owner: XrefPropertyValue
    domain_of:
    - PropertyValue
    range: string
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: xrefs
    owner: XrefPropertyValue
    domain_of:
    - Meta
    - PropertyValue
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: XrefPropertyValue
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta

```
</details>