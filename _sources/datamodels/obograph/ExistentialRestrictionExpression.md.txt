# Class: ExistentialRestrictionExpression
_An existential restriction (OWL some values from) expression_




URI: [owl:Restriction](http://www.w3.org/2002/07/owl#Restriction)



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
| [fillerId](fillerId.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |
| [propertyId](propertyId.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | [restrictions](restrictions.md) | range | [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) |




## Aliases


* some values from expression



## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | ObjectSomeValuesFrom({propertyId} {fillerId}) |



### Schema Source


* from schema: https://github.com/geneontology/obographs





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:Restriction |
| native | og:ExistentialRestrictionExpression |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ExistentialRestrictionExpression
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ObjectSomeValuesFrom({propertyId} {fillerId})
description: An existential restriction (OWL some values from) expression
from_schema: https://github.com/geneontology/obographs
aliases:
- some values from expression
rank: 1000
slots:
- fillerId
- propertyId
class_uri: owl:Restriction

```
</details>

### Induced

<details>
```yaml
name: ExistentialRestrictionExpression
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ObjectSomeValuesFrom({propertyId} {fillerId})
description: An existential restriction (OWL some values from) expression
from_schema: https://github.com/geneontology/obographs
aliases:
- some values from expression
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
class_uri: owl:Restriction

```
</details>