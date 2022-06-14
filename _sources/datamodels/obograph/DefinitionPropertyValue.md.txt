# Class: DefinitionPropertyValue




URI: [og:DefinitionPropertyValue](https://github.com/geneontology/obographs/DefinitionPropertyValue)




```{mermaid}
 classDiagram
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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [pred](pred.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [val](val.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [xrefs](xrefs.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Meta](Meta.md) | [definition](definition.md) | range | DefinitionPropertyValue |



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:DefinitionPropertyValue'] |
| native | ['og:DefinitionPropertyValue'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DefinitionPropertyValue
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue

```
</details>

### Induced

<details>
```yaml
name: DefinitionPropertyValue
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
attributes:
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    alias: pred
    owner: DefinitionPropertyValue
    range: string
  val:
    name: val
    from_schema: https://github.com/geneontology/obographs
    alias: val
    owner: DefinitionPropertyValue
    range: string
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: xrefs
    owner: DefinitionPropertyValue
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: DefinitionPropertyValue
    range: Meta

```
</details>