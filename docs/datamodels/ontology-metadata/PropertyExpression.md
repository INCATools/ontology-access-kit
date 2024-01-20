# Class: PropertyExpression



URI: [omoschema:PropertyExpression](http://purl.obolibrary.org/obo/omo/schema/PropertyExpression)



```{mermaid}
 classDiagram
    class PropertyExpression
      Expression <|-- PropertyExpression
      

      PropertyExpression <|-- ObjectProperty
      
      
      PropertyExpression : disjointWith
        
      
```





## Inheritance
* [Expression](Expression.md)
    * **PropertyExpression**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [disjointWith](disjointWith.md) | 0..* <br/> [String](String.md) |  | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [ObjectProperty](ObjectProperty.md) | A property that connects two objects in logical axioms |




## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Restriction](Restriction.md) | [onProperty](onProperty.md) | range | [PropertyExpression](PropertyExpression.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:PropertyExpression |
| native | omoschema:PropertyExpression |





## LinkML Source

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