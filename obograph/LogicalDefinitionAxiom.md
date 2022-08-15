# Class: LogicalDefinitionAxiom




URI: [og:LogicalDefinitionAxiom](https://github.com/geneontology/obographs/LogicalDefinitionAxiom)




```{mermaid}
 classDiagram
      Axiom <|-- LogicalDefinitionAxiom
      
      LogicalDefinitionAxiom : meta
      

```





## Inheritance
* [Axiom](Axiom.md)
    * **LogicalDefinitionAxiom**



## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [meta](meta.md) | 0..1 <br/> [Meta](Meta.md)  |   |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [logicalDefinitionAxioms](logicalDefinitionAxioms.md) | range | LogicalDefinitionAxiom |



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:LogicalDefinitionAxiom'] |
| native | ['og:LogicalDefinitionAxiom'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LogicalDefinitionAxiom
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: Axiom

```
</details>

### Induced

<details>
```yaml
name: LogicalDefinitionAxiom
from_schema: https://github.com/geneontology/obographs
rank: 1000
is_a: Axiom
attributes:
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: meta
    owner: LogicalDefinitionAxiom
    domain_of:
    - GraphDocument
    - Graph
    - Node
    - PropertyValue
    - Axiom
    range: Meta

```
</details>