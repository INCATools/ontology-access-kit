# Class: SynonymPropertyValue



URI: [og:SynonymPropertyValue](https://github.com/geneontology/obographs/SynonymPropertyValue)


```{mermaid}
 classDiagram
    class SynonymPropertyValue
      PropertyValue <|-- SynonymPropertyValue
      
      SynonymPropertyValue : isExact
      SynonymPropertyValue : meta
      SynonymPropertyValue : pred
      SynonymPropertyValue : synonymType
      SynonymPropertyValue : val
      SynonymPropertyValue : xrefs
      
```




## Inheritance
* [PropertyValue](PropertyValue.md)
    * **SynonymPropertyValue**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [synonymType](synonymType.md) | 0..1 <br/> string | None | direct |
| [isExact](isExact.md) | 0..1 <br/> boolean | None | direct |
| [pred](pred.md) | 0..1 <br/> string | None | direct |
| [xrefs](xrefs.md) | 0..* <br/> string | None | [PropertyValue](PropertyValue.md) |
| [val](val.md) | 0..1 <br/> string | None | [PropertyValue](PropertyValue.md) |
| [meta](meta.md) | 0..1 <br/> Meta | None | [PropertyValue](PropertyValue.md) |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Meta](Meta.md) | [synonyms](synonyms.md) | range | SynonymPropertyValue |







## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | og:SynonymPropertyValue |
| native | og:SynonymPropertyValue |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SynonymPropertyValue
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
slots:
- synonymType
- isExact
- pred
slot_usage:
  pred:
    name: pred
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: ScopeEnum

```
</details>

### Induced

<details>
```yaml
name: SynonymPropertyValue
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: PropertyValue
slot_usage:
  pred:
    name: pred
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: ScopeEnum
attributes:
  synonymType:
    name: synonymType
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: synonymType
    owner: SynonymPropertyValue
    domain_of:
    - SynonymPropertyValue
    range: string
  isExact:
    name: isExact
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: isExact
    owner: SynonymPropertyValue
    domain_of:
    - SynonymPropertyValue
    range: boolean
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: pred
    owner: SynonymPropertyValue
    domain_of:
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    - Edge
    - SynonymPropertyValue
    - PropertyValue
    range: ScopeEnum
  val:
    name: val
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: val
    owner: SynonymPropertyValue
    domain_of:
    - PropertyValue
    range: string
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    multivalued: true
    alias: xrefs
    owner: SynonymPropertyValue
    domain_of:
    - Meta
    - PropertyValue
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: SynonymPropertyValue
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta

```
</details>