# Class: PropertyExpression



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:PropertyExpression](http://purl.obolibrary.org/obo/schema/PropertyExpression)




```{mermaid}
 classDiagram
      Expression <|-- PropertyExpression
      
      PropertyExpression : disjointWith
      

```





## Inheritance
* [Expression](Expression.md)
    * **PropertyExpression**



## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [disjointWith](disjointWith.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Restriction](Restriction.md) | [onProperty](onProperty.md) | range | PropertyExpression |



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['omoschema:PropertyExpression'] |
| native | ['omoschema:PropertyExpression'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyExpression
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: Expression
mixin: true
slots:
- disjointWith

```
</details>

### Induced

<details>
```yaml
name: PropertyExpression
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: Expression
mixin: true
attributes:
  disjointWith:
    name: disjointWith
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:disjointWith
    multivalued: true
    alias: disjointWith
    owner: PropertyExpression
    domain_of:
    - ClassExpression
    - PropertyExpression
    range: string

```
</details>