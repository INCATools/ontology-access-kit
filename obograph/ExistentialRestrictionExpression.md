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

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [fillerId](fillerId.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [propertyId](propertyId.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://github.com/geneontology/obographs







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['og:ExistentialRestrictionExpression'] |
| native | ['og:ExistentialRestrictionExpression'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ExistentialRestrictionExpression
from_schema: https://github.com/geneontology/obographs
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
attributes:
  fillerId:
    name: fillerId
    from_schema: https://github.com/geneontology/obographs
    alias: fillerId
    owner: ExistentialRestrictionExpression
    range: string
  propertyId:
    name: propertyId
    from_schema: https://github.com/geneontology/obographs
    alias: propertyId
    owner: ExistentialRestrictionExpression
    range: string

```
</details>