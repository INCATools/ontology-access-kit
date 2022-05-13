# Class: Axiom


* __NOTE__: this is an abstract class and should not be instantiated directly



URI: [og:Axiom](https://github.com/geneontology/obographs/Axiom)




## Inheritance

* **Axiom**
    * [DomainRangeAxiom](DomainRangeAxiom.md)
    * [EquivalentNodesSet](EquivalentNodesSet.md)
    * [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md)
    * [PropertyChainAxiom](PropertyChainAxiom.md)




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Axiom
from_schema: https://github.com/geneontology/obographs
abstract: true
slots:
- meta

```
</details>

### Induced

<details>
```yaml
name: Axiom
from_schema: https://github.com/geneontology/obographs
abstract: true
attributes:
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: Axiom
    range: Meta

```
</details>