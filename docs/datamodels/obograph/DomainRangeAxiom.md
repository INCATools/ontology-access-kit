# Class: DomainRangeAxiom




URI: [og:DomainRangeAxiom](https://github.com/geneontology/obographs/DomainRangeAxiom)




```{mermaid}
 classDiagram
      Axiom <|-- DomainRangeAxiom
      
      DomainRangeAxiom : meta
      

```





## Inheritance
* [Axiom](Axiom.md)
    * **DomainRangeAxiom**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [domainRangeAxioms](domainRangeAxioms.md) | range | DomainRangeAxiom |



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:DomainRangeAxiom'] |
| native | ['og:DomainRangeAxiom'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DomainRangeAxiom
from_schema: https://github.com/geneontology/obographs
is_a: Axiom

```
</details>

### Induced

<details>
```yaml
name: DomainRangeAxiom
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
attributes:
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: DomainRangeAxiom
    range: Meta

```
</details>