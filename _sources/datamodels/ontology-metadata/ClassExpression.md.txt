# Class: ClassExpression



URI: [omoschema:ClassExpression](http://purl.obolibrary.org/obo/omo/schema/ClassExpression)



```{mermaid}
 classDiagram
    class ClassExpression
      Expression <|-- ClassExpression
      

      ClassExpression <|-- Class
      ClassExpression <|-- Restriction
      
      
      ClassExpression : cardinality
        
      ClassExpression : complementOf
        
      ClassExpression : disjointWith
        
      ClassExpression : equivalentClass
        
          ClassExpression ..> ClassExpression : equivalentClass
        
      ClassExpression : intersectionOf
        
          ClassExpression ..> ClassExpression : intersectionOf
        
      ClassExpression : oneOf
        
          ClassExpression ..> ClassExpression : oneOf
        
      ClassExpression : subClassOf
        
          ClassExpression ..> ClassExpression : subClassOf
        
      ClassExpression : unionOf
        
      
```





## Inheritance
* [Expression](Expression.md)
    * **ClassExpression**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [disjointWith](disjointWith.md) | 0..* <br/> [String](String.md) |  | direct |
| [equivalentClass](equivalentClass.md) | 0..* <br/> [ClassExpression](ClassExpression.md) |  | direct |
| [intersectionOf](intersectionOf.md) | 0..1 <br/> [ClassExpression](ClassExpression.md) |  | direct |
| [subClassOf](subClassOf.md) | 0..* <br/> [ClassExpression](ClassExpression.md) |  | direct |
| [cardinality](cardinality.md) | 0..1 <br/> [String](String.md) |  | direct |
| [complementOf](complementOf.md) | 0..1 <br/> [String](String.md) |  | direct |
| [oneOf](oneOf.md) | 0..1 <br/> [ClassExpression](ClassExpression.md) |  | direct |
| [unionOf](unionOf.md) | 0..1 <br/> [String](String.md) |  | direct |



## Mixin Usage

| mixed into | description |
| --- | --- |
| [Class](Class.md) |  |
| [Restriction](Restriction.md) |  |




## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Class](Class.md) | [equivalentClass](equivalentClass.md) | range | [ClassExpression](ClassExpression.md) |
| [Class](Class.md) | [intersectionOf](intersectionOf.md) | range | [ClassExpression](ClassExpression.md) |
| [Class](Class.md) | [oneOf](oneOf.md) | range | [ClassExpression](ClassExpression.md) |
| [Restriction](Restriction.md) | [equivalentClass](equivalentClass.md) | range | [ClassExpression](ClassExpression.md) |
| [Restriction](Restriction.md) | [intersectionOf](intersectionOf.md) | range | [ClassExpression](ClassExpression.md) |
| [Restriction](Restriction.md) | [subClassOf](subClassOf.md) | range | [ClassExpression](ClassExpression.md) |
| [Restriction](Restriction.md) | [oneOf](oneOf.md) | range | [ClassExpression](ClassExpression.md) |
| [ClassExpression](ClassExpression.md) | [equivalentClass](equivalentClass.md) | range | [ClassExpression](ClassExpression.md) |
| [ClassExpression](ClassExpression.md) | [intersectionOf](intersectionOf.md) | range | [ClassExpression](ClassExpression.md) |
| [ClassExpression](ClassExpression.md) | [subClassOf](subClassOf.md) | range | [ClassExpression](ClassExpression.md) |
| [ClassExpression](ClassExpression.md) | [oneOf](oneOf.md) | range | [ClassExpression](ClassExpression.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:ClassExpression |
| native | omoschema:ClassExpression |





## LinkML Source

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