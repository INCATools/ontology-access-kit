# Class: PropertyChainAxiom




URI: [og:PropertyChainAxiom](https://github.com/geneontology/obographs/PropertyChainAxiom)




## Inheritance

* [Axiom](Axiom.md)
    * **PropertyChainAxiom**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [propertyChainAxioms](propertyChainAxioms.md) | range | PropertyChainAxiom |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyChainAxiom
from_schema: https://github.com/geneontology/obographs
is_a: Axiom

```
</details>

### Induced

<details>
```yaml
name: PropertyChainAxiom
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
attributes:
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: PropertyChainAxiom
    range: Meta

```
</details>