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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [pred](pred.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [val](val.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [xrefs](xrefs.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


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
is_a: PropertyValue

```
</details>

### Induced

<details>
```yaml
name: XrefPropertyValue
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
attributes:
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    alias: pred
    owner: XrefPropertyValue
    range: string
  val:
    name: val
    from_schema: https://github.com/geneontology/obographs
    alias: val
    owner: XrefPropertyValue
    range: string
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: xrefs
    owner: XrefPropertyValue
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: XrefPropertyValue
    range: Meta

```
</details>