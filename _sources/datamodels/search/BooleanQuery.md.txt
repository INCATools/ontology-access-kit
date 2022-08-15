# Class: BooleanQuery




URI: [search:BooleanQuery](https://w3id.org/linkml/search_datamodel/BooleanQuery)




```{mermaid}
 classDiagram
    class BooleanQuery
      BooleanQuery : atom
      BooleanQuery : operands
      BooleanQuery : operator
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [operator](operator.md) | 0..1 <br/> [BooleanOperator](BooleanOperator.md)  |   |
| [operands](operands.md) | 0..* <br/> [BooleanQuery](BooleanQuery.md)  |   |
| [atom](atom.md) | 0..1 <br/> [AtomicQuery](AtomicQuery.md)  |   |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [BooleanQuery](BooleanQuery.md) | [operands](operands.md) | range | BooleanQuery |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/search_datamodel







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['search:BooleanQuery'] |
| native | ['search:BooleanQuery'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: BooleanQuery
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
attributes:
  operator:
    name: operator
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: BooleanOperator
  operands:
    name: operands
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    range: BooleanQuery
  atom:
    name: atom
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    range: AtomicQuery

```
</details>

### Induced

<details>
```yaml
name: BooleanQuery
from_schema: https://w3id.org/linkml/search_datamodel
rank: 1000
attributes:
  operator:
    name: operator
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: operator
    owner: BooleanQuery
    domain_of:
    - BooleanQuery
    range: BooleanOperator
  operands:
    name: operands
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    multivalued: true
    alias: operands
    owner: BooleanQuery
    domain_of:
    - BooleanQuery
    range: BooleanQuery
  atom:
    name: atom
    from_schema: https://w3id.org/linkml/search_datamodel
    rank: 1000
    alias: atom
    owner: BooleanQuery
    domain_of:
    - BooleanQuery
    range: AtomicQuery

```
</details>