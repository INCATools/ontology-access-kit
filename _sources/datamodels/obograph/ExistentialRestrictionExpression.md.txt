# Class: ExistentialRestrictionExpression



URI: [og:ExistentialRestrictionExpression](https://github.com/geneontology/obographs/ExistentialRestrictionExpression)


```{mermaid}
 classDiagram
    class ExistentialRestrictionExpression
      ExistentialRestrictionExpression : fillerId
      ExistentialRestrictionExpression : propertyId
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [fillerId](fillerId.md) | 0..1 <br/> string | None | direct |
| [propertyId](propertyId.md) | 0..1 <br/> string | None | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | [restrictions](restrictions.md) | range | ExistentialRestrictionExpression |







## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | og:ExistentialRestrictionExpression |
| native | og:ExistentialRestrictionExpression |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ExistentialRestrictionExpression
from_schema: https://github.com/geneontology/obographs
rank: 1000
slots:
- fillerId
- propertyId

```
</details>

### Induced

<details>
```yaml
name: ExistentialRestrictionExpression
from_schema: https://github.com/geneontology/obographs
rank: 1000
attributes:
  fillerId:
    name: fillerId
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: fillerId
    owner: ExistentialRestrictionExpression
    domain_of:
    - ExistentialRestrictionExpression
    range: string
  propertyId:
    name: propertyId
    from_schema: https://github.com/geneontology/obographs
    rank: 1000
    alias: propertyId
    owner: ExistentialRestrictionExpression
    domain_of:
    - ExistentialRestrictionExpression
    range: string

```
</details>