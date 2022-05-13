# Class: PropertyExpression



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:PropertyExpression](http://purl.obolibrary.org/obo/schema/PropertyExpression)




## Inheritance

* [Expression](Expression.md)
    * **PropertyExpression**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [disjointWith](disjointWith.md) | [string](string.md) | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Restriction](Restriction.md) | [onProperty](onProperty.md) | range | PropertyExpression |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: PropertyExpression
from_schema: http://purl.obolibrary.org/obo/omo/schema
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
is_a: Expression
mixin: true
attributes:
  disjointWith:
    name: disjointWith
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:disjointWith
    multivalued: true
    alias: disjointWith
    owner: PropertyExpression
    range: string

```
</details>