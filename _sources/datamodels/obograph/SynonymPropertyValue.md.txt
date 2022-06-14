# Class: SynonymPropertyValue




URI: [og:SynonymPropertyValue](https://github.com/geneontology/obographs/SynonymPropertyValue)




```{mermaid}
 classDiagram
      PropertyValue <|-- SynonymPropertyValue
      
      SynonymPropertyValue : isExact
      SynonymPropertyValue : meta
      SynonymPropertyValue : pred
      SynonymPropertyValue : scope
      SynonymPropertyValue : synonymType
      SynonymPropertyValue : val
      SynonymPropertyValue : xrefs
      

```





## Inheritance
* [PropertyValue](PropertyValue.md)
    * **SynonymPropertyValue**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [synonymType](synonymType.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [isExact](isExact.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [scope](scope.md) | [ScopesEnum](ScopesEnum.md) | 0..1 | None  | . |
| [pred](pred.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [val](val.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [xrefs](xrefs.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


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
| self | ['og:SynonymPropertyValue'] |
| native | ['og:SynonymPropertyValue'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: SynonymPropertyValue
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
slots:
- synonymType
- isExact
- scope

```
</details>

### Induced

<details>
```yaml
name: SynonymPropertyValue
from_schema: https://github.com/geneontology/obographs
is_a: PropertyValue
attributes:
  synonymType:
    name: synonymType
    from_schema: https://github.com/geneontology/obographs
    alias: synonymType
    owner: SynonymPropertyValue
    range: string
  isExact:
    name: isExact
    from_schema: https://github.com/geneontology/obographs
    alias: isExact
    owner: SynonymPropertyValue
    range: boolean
  scope:
    name: scope
    from_schema: https://github.com/geneontology/obographs
    alias: scope
    owner: SynonymPropertyValue
    range: scopes_enum
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    alias: pred
    owner: SynonymPropertyValue
    range: string
  val:
    name: val
    from_schema: https://github.com/geneontology/obographs
    alias: val
    owner: SynonymPropertyValue
    range: string
  xrefs:
    name: xrefs
    from_schema: https://github.com/geneontology/obographs
    multivalued: true
    alias: xrefs
    owner: SynonymPropertyValue
    range: string
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: SynonymPropertyValue
    range: Meta

```
</details>