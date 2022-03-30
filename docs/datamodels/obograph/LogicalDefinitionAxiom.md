# Class: LogicalDefinitionAxiom




URI: [og:LogicalDefinitionAxiom](https://github.com/geneontology/obographs/LogicalDefinitionAxiom)




## Inheritance

* [Axiom](Axiom.md)
    * **LogicalDefinitionAxiom**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [meta](meta.md) | [Meta](Meta.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Graph](Graph.md) | [logicalDefinitionAxioms](logicalDefinitionAxioms.md) | range | LogicalDefinitionAxiom |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: LogicalDefinitionAxiom
from_schema: https://github.com/geneontology/obographs
is_a: Axiom

```
</details>

### Induced

<details>
```yaml
name: LogicalDefinitionAxiom
from_schema: https://github.com/geneontology/obographs
is_a: Axiom
attributes:
  meta:
    name: meta
    from_schema: https://github.com/geneontology/obographs
    alias: meta
    owner: LogicalDefinitionAxiom
    range: Meta

```
</details>