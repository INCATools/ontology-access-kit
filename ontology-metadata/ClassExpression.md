# Class: ClassExpression



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:ClassExpression](http://purl.obolibrary.org/obo/schema/ClassExpression)




```{mermaid}
 classDiagram
      Expression <|-- ClassExpression
      
      ClassExpression : cardinality
      ClassExpression : complementOf
      ClassExpression : disjointWith
      ClassExpression : equivalentClass
      ClassExpression : intersectionOf
      ClassExpression : oneOf
      ClassExpression : subClassOf
      ClassExpression : unionOf
      

```





## Inheritance
* [Expression](Expression.md)
    * **ClassExpression**



## Slots

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [disjointWith](disjointWith.md) | 0..* <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [equivalentClass](equivalentClass.md) | 0..* <br/> [ClassExpression](ClassExpression.md)  |   |
| [intersectionOf](intersectionOf.md) | 0..1 <br/> [ClassExpression](ClassExpression.md)  |   |
| [subClassOf](subClassOf.md) | 0..* <br/> [ClassExpression](ClassExpression.md)  |   |
| [cardinality](cardinality.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [complementOf](complementOf.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |
| [oneOf](oneOf.md) | 0..1 <br/> [ClassExpression](ClassExpression.md)  |   |
| [unionOf](unionOf.md) | 0..1 <br/> [xsd:string](http://www.w3.org/2001/XMLSchema#string)  |   |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Class](Class.md) | [equivalentClass](equivalentClass.md) | range | ClassExpression |
| [Class](Class.md) | [intersectionOf](intersectionOf.md) | range | ClassExpression |
| [Class](Class.md) | [oneOf](oneOf.md) | range | ClassExpression |
| [Restriction](Restriction.md) | [equivalentClass](equivalentClass.md) | range | ClassExpression |
| [Restriction](Restriction.md) | [intersectionOf](intersectionOf.md) | range | ClassExpression |
| [Restriction](Restriction.md) | [subClassOf](subClassOf.md) | range | ClassExpression |
| [Restriction](Restriction.md) | [oneOf](oneOf.md) | range | ClassExpression |
| [ClassExpression](ClassExpression.md) | [equivalentClass](equivalentClass.md) | range | ClassExpression |
| [ClassExpression](ClassExpression.md) | [intersectionOf](intersectionOf.md) | range | ClassExpression |
| [ClassExpression](ClassExpression.md) | [subClassOf](subClassOf.md) | range | ClassExpression |
| [ClassExpression](ClassExpression.md) | [oneOf](oneOf.md) | range | ClassExpression |



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['omoschema:ClassExpression'] |
| native | ['omoschema:ClassExpression'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ClassExpression
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
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
    owner: ClassExpression
    domain_of:
    - ClassExpression
    - PropertyExpression
    range: string
  equivalentClass:
    name: equivalentClass
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    mixins:
    - match_aspect
    slot_uri: owl:equivalentClass
    multivalued: true
    alias: equivalentClass
    owner: ClassExpression
    domain_of:
    - ClassExpression
    range: ClassExpression
  intersectionOf:
    name: intersectionOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:intersectionOf
    alias: intersectionOf
    owner: ClassExpression
    domain_of:
    - ClassExpression
    range: ClassExpression
  subClassOf:
    name: subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:subClassOf
    multivalued: true
    alias: subClassOf
    owner: ClassExpression
    domain_of:
    - ClassExpression
    range: ClassExpression
  cardinality:
    name: cardinality
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:cardinality
    alias: cardinality
    owner: ClassExpression
    domain_of:
    - ClassExpression
    range: string
  complementOf:
    name: complementOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:complementOf
    alias: complementOf
    owner: ClassExpression
    domain_of:
    - ClassExpression
    range: string
  oneOf:
    name: oneOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:oneOf
    alias: oneOf
    owner: ClassExpression
    domain_of:
    - ClassExpression
    range: ClassExpression
  unionOf:
    name: unionOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:unionOf
    alias: unionOf
    owner: ClassExpression
    domain_of:
    - ClassExpression
    range: string

```
</details>