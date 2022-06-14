# Class: Restriction



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [owl:Restriction](http://www.w3.org/2002/07/owl#Restriction)




```{mermaid}
 classDiagram
      ClassExpression <|-- Restriction
      AnonymousClassExpression <|-- Restriction
      
      Restriction : allValuesFrom
      Restriction : cardinality
      Restriction : complementOf
      Restriction : disjointWith
      Restriction : equivalentClass
      Restriction : intersectionOf
      Restriction : oneOf
      Restriction : onProperty
      Restriction : someValuesFrom
      Restriction : subClassOf
      Restriction : unionOf
      

```





## Inheritance
* [Anonymous](Anonymous.md)
    * [AnonymousClassExpression](AnonymousClassExpression.md)
        * **Restriction** [ ClassExpression]



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [onProperty](onProperty.md) | [PropertyExpression](PropertyExpression.md) | 0..* | None  | . |
| [someValuesFrom](someValuesFrom.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [allValuesFrom](allValuesFrom.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [disjointWith](disjointWith.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [equivalentClass](equivalentClass.md) | [ClassExpression](ClassExpression.md) | 0..* | None  | . |
| [intersectionOf](intersectionOf.md) | [ClassExpression](ClassExpression.md) | 0..1 | None  | . |
| [subClassOf](subClassOf.md) | [ClassExpression](ClassExpression.md) | 0..* | None  | . |
| [cardinality](cardinality.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [complementOf](complementOf.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [oneOf](oneOf.md) | [ClassExpression](ClassExpression.md) | 0..1 | None  | . |
| [unionOf](unionOf.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['owl:Restriction'] |
| native | ['omoschema:Restriction'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Restriction
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnonymousClassExpression
mixin: true
mixins:
- ClassExpression
slots:
- onProperty
- someValuesFrom
- allValuesFrom
class_uri: owl:Restriction

```
</details>

### Induced

<details>
```yaml
name: Restriction
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnonymousClassExpression
mixin: true
mixins:
- ClassExpression
attributes:
  onProperty:
    name: onProperty
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:onProperty
    multivalued: true
    alias: onProperty
    owner: Restriction
    range: PropertyExpression
  someValuesFrom:
    name: someValuesFrom
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:someValuesFrom
    multivalued: true
    alias: someValuesFrom
    owner: Restriction
    range: string
  allValuesFrom:
    name: allValuesFrom
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:allValuesFrom
    alias: allValuesFrom
    owner: Restriction
    range: string
  disjointWith:
    name: disjointWith
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:disjointWith
    multivalued: true
    alias: disjointWith
    owner: Restriction
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
    owner: Restriction
    range: ClassExpression
  intersectionOf:
    name: intersectionOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:intersectionOf
    alias: intersectionOf
    owner: Restriction
    range: ClassExpression
  subClassOf:
    name: subClassOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: rdfs:subClassOf
    multivalued: true
    alias: subClassOf
    owner: Restriction
    range: ClassExpression
  cardinality:
    name: cardinality
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:cardinality
    alias: cardinality
    owner: Restriction
    range: string
  complementOf:
    name: complementOf
    todos:
    - restrict range
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:complementOf
    alias: complementOf
    owner: Restriction
    range: string
  oneOf:
    name: oneOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:oneOf
    alias: oneOf
    owner: Restriction
    range: ClassExpression
  unionOf:
    name: unionOf
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: logical_predicate
    slot_uri: owl:unionOf
    alias: unionOf
    owner: Restriction
    range: string
class_uri: owl:Restriction

```
</details>