# Class: DefinitionPropertyValue



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
| ---  | --- | --- | --- || [val](val.md) | 0..1 <br/> string | None | [PropertyValue](PropertyValue.md) |
| [meta](meta.md) | 0..1 <br/> Meta | None | [PropertyValue](PropertyValue.md) |
| [xrefs](xrefs.md) | 0..* <br/> string | None | [PropertyValue](PropertyValue.md) |
| [pred](pred.md) | 0..1 <br/> string | None | [PropertyValue](PropertyValue.md) |



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
| self | og:DefinitionPropertyValue |
| native | og:DefinitionPropertyValue |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DefinitionPropertyValue
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue

```
</details>

### Induced

<details>
```yaml
name: DefinitionPropertyValue
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
attributes:
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: pred
    owner: DefinitionPropertyValue
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: string
  val:
    name: val
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: val
    owner: DefinitionPropertyValue
    domain_of:
    - PropertyValue
    range: string
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: xrefs
    owner: DefinitionPropertyValue
    domain_of:
    - Meta
    - PropertyValue
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: DefinitionPropertyValue
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta

```
</details>