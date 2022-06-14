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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [operator](operator.md) | [BooleanOperator](BooleanOperator.md) | 0..1 | None  | . |
| [operands](operands.md) | [BooleanQuery](BooleanQuery.md) | 0..* | None  | . |
| [atom](atom.md) | [AtomicQuery](AtomicQuery.md) | 0..1 | None  | . |


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
attributes:
  operator:
    name: operator
    from_schema: https://w3id.org/linkml/search_datamodel
    range: BooleanOperator
  operands:
    name: operands
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true
    range: BooleanQuery
  atom:
    name: atom
    from_schema: https://w3id.org/linkml/search_datamodel
    range: AtomicQuery

```
</details>

### Induced

<details>
```yaml
name: BooleanQuery
from_schema: https://w3id.org/linkml/search_datamodel
attributes:
  operator:
    name: operator
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: operator
    owner: BooleanQuery
    range: BooleanOperator
  operands:
    name: operands
    from_schema: https://w3id.org/linkml/search_datamodel
    multivalued: true
    alias: operands
    owner: BooleanQuery
    range: BooleanQuery
  atom:
    name: atom
    from_schema: https://w3id.org/linkml/search_datamodel
    alias: atom
    owner: BooleanQuery
    range: AtomicQuery

```
</details>