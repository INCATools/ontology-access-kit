

# Class: ExistentialRestrictionExpression


_An existential restriction (OWL some values from) expression_





URI: [owl:Restriction](http://www.w3.org/2002/07/owl#Restriction)






```{mermaid}
 classDiagram
    class ExistentialRestrictionExpression
    click ExistentialRestrictionExpression href "../ExistentialRestrictionExpression"
      ExistentialRestrictionExpression : fillerId
        
      ExistentialRestrictionExpression : propertyId
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [fillerId](fillerId.md) | 0..1 <br/> [String](String.md) | in an OWL restriction expression, the filler is the object of the restriction | direct |
| [propertyId](propertyId.md) | 0..1 <br/> [String](String.md) | in an OWL restriction expression, this is the predicate | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [LogicalDefinitionAxiom](LogicalDefinitionAxiom.md) | [restrictions](restrictions.md) | range | [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) |
| [DisjointClassExpressionsAxiom](DisjointClassExpressionsAxiom.md) | [classExpressions](classExpressions.md) | range | [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) |
| [DisjointClassExpressionsAxiom](DisjointClassExpressionsAxiom.md) | [unionEquivalentToExpression](unionEquivalentToExpression.md) | range | [ExistentialRestrictionExpression](ExistentialRestrictionExpression.md) |




## Aliases


* some values from expression



## Comments

* note that most existing restrictions are present in simple A SubClassOf R some B axioms, which are translated to *edges* in a graph. This class exists for other cases that do not map to edges.

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
| native | obographs:ExistentialRestrictionExpression |







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
comments:
- note that most existing restrictions are present in simple A SubClassOf R some B
  axioms, which are translated to *edges* in a graph. This class exists for other
  cases that do not map to edges.
from_schema: https://github.com/geneontology/obographs
aliases:
- some values from expression
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
comments:
- note that most existing restrictions are present in simple A SubClassOf R some B
  axioms, which are translated to *edges* in a graph. This class exists for other
  cases that do not map to edges.
from_schema: https://github.com/geneontology/obographs
aliases:
- some values from expression
attributes:
  fillerId:
    name: fillerId
    description: in an OWL restriction expression, the filler is the object of the
      restriction
    from_schema: https://github.com/geneontology/obographs
    aliases:
    - object
    rank: 1000
    alias: fillerId
    owner: ExistentialRestrictionExpression
    domain_of:
    - ExistentialRestrictionExpression
    range: string
  propertyId:
    name: propertyId
    description: in an OWL restriction expression, this is the predicate
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