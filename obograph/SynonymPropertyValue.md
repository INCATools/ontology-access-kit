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

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [synonymType](synonymType.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [isExact](isExact.md) | 0..1 <br/> [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean)  |   |
| [scope](scope.md) | 0..1 <br/> [ScopesEnum](ScopesEnum.md)  |   |
| [pred](pred.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [val](val.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [xrefs](xrefs.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md)  |   |


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
rank: 1000
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
rank: 1000
is_a: PropertyValue
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
  scope:
    name: scope
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: scope
    owner: SynonymPropertyValue
    domain_of:
    - SynonymPropertyValue
    range: scopes_enum
  pred:
    name: pred
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: pred
    owner: SynonymPropertyValue
    domain_of:
    - Edge
    - PropertyValue
    range: string
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