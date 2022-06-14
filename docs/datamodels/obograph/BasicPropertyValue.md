# Class: BasicPropertyValue




URI: [og:BasicPropertyValue](https://github.com/geneontology/obographs/BasicPropertyValue)




```{mermaid}
 classDiagram
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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [pred](pred.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [val](val.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [xrefs](xrefs.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Meta](Meta.md) | [basicPropertyValues](basicPropertyValues.md) | range | BasicPropertyValue |



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:BasicPropertyValue'] |
| native | ['og:BasicPropertyValue'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: BasicPropertyValue
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue

```
</details>

### Induced

<details>
```yaml
name: BasicPropertyValue
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
attributes:
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    alias: pred
    owner: BasicPropertyValue
    range: string
  val:
    name: val
    from_schema: https://github.com/geneontology/obographs
    alias: val
    owner: BasicPropertyValue
    range: string
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: xrefs
    owner: BasicPropertyValue
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: BasicPropertyValue
    range: Meta

```
</details>