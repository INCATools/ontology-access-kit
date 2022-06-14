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
| self | ['og:PropertyValue'] |
| native | ['og:PropertyValue'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyValue
from_schema: https://github.com/geneontology/obographs
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
abstract: true
attributes:
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    alias: pred
    owner: PropertyValue
    range: string
  val:
    name: val
    from_schema: https://github.com/geneontology/obographs
    alias: val
    owner: PropertyValue
    range: string
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: xrefs
    owner: PropertyValue
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: PropertyValue
    range: Meta

```
</details>