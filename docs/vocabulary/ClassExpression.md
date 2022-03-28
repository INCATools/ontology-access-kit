# Class: ClassExpression



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:ClassExpression](http://purl.obolibrary.org/obo/schema/ClassExpression)




## Inheritance

* [Expression](Expression.md)
    * **ClassExpression**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [disjointWith](disjointWith.md) | [string](string.md) | 0..* | None  | . |
| [equivalentClass](equivalentClass.md) | [string](string.md) | 0..* | None  | . |
| [intersectionOf](intersectionOf.md) | [string](string.md) | 0..1 | None  | . |
| [subClassOf](subClassOf.md) | [ClassExpression](ClassExpression.md) | 0..* | None  | . |
| [cardinality](cardinality.md) | [string](string.md) | 0..1 | None  | . |
| [complementOf](complementOf.md) | [string](string.md) | 0..1 | None  | . |
| [oneOf](oneOf.md) | [ClassExpression](ClassExpression.md) | 0..1 | None  | . |
| [unionOf](unionOf.md) | [string](string.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Class](Class.md) | [oneOf](oneOf.md) | range | ClassExpression |
| [NamedIndividual](NamedIndividual.md) | [type](type.md) | range | ClassExpression |
| [Restriction](Restriction.md) | [subClassOf](subClassOf.md) | range | ClassExpression |
| [Restriction](Restriction.md) | [oneOf](oneOf.md) | range | ClassExpression |
| [ClassExpression](ClassExpression.md) | [subClassOf](subClassOf.md) | range | ClassExpression |
| [ClassExpression](ClassExpression.md) | [oneOf](oneOf.md) | range | ClassExpression |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ClassExpression
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: Expression
mixin: true
slots:
- disjointWith
- equivalentClass
- intersectionOf
- subClassOf
- cardinality
- complementOf
- oneOf
- unionOf

```
</details>

### Induced

<details>
```yaml
name: ClassExpression
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
    owner: ClassExpression
    range: string
  equivalentClass:
    name: equivalentClass
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    mixins:
    - match_aspect
    slot_uri: owl:equivalentClass
    multivalued: true
    alias: equivalentClass
    owner: ClassExpression
    range: string
  intersectionOf:
    name: intersectionOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:intersectionOf
    alias: intersectionOf
    owner: ClassExpression
    range: string
  subClassOf:
    name: subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: rdfs:subClassOf
    multivalued: true
    alias: subClassOf
    owner: ClassExpression
    range: ClassExpression
  cardinality:
    name: cardinality
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:cardinality
    alias: cardinality
    owner: ClassExpression
    range: string
  complementOf:
    name: complementOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:complementOf
    alias: complementOf
    owner: ClassExpression
    range: string
  oneOf:
    name: oneOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:oneOf
    alias: oneOf
    owner: ClassExpression
    range: ClassExpression
  unionOf:
    name: unionOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:unionOf
    alias: unionOf
    owner: ClassExpression
    range: string

```
</details>