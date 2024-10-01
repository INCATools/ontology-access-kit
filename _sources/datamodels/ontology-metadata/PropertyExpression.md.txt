

# Class: PropertyExpression



URI: [omoschema:PropertyExpression](https://w3id.org/oak/ontology-metadata/PropertyExpression)






```{mermaid}
 classDiagram
    class PropertyExpression
    click PropertyExpression href "../PropertyExpression"
      Expression <|-- PropertyExpression
        click Expression href "../Expression"
      

      PropertyExpression <|-- ObjectProperty
        click ObjectProperty href "../ObjectProperty"
      
      
      PropertyExpression : disjointWith
        
      
```





## Inheritance
* [Expression](Expression.md)
    * **PropertyExpression**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [disjointWith](disjointWith.md) | * <br/> [String](String.md) |  | direct |



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


* from schema: https://w3id.org/oak/ontology-metadata




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
from_schema: https://w3id.org/oak/ontology-metadata
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
from_schema: https://w3id.org/oak/ontology-metadata
is_a: Expression
mixin: true
attributes:
  disjointWith:
    name: disjointWith
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:disjointWith
    alias: disjointWith
    owner: PropertyExpression
    domain_of:
    - ClassExpression
    - PropertyExpression
    range: string
    multivalued: true

```
</details>