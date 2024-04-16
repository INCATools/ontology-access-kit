

# Class: Restriction



URI: [owl:Restriction](http://www.w3.org/2002/07/owl#Restriction)




```{mermaid}
 classDiagram
    class Restriction
      ClassExpression <|-- Restriction
      AnonymousClassExpression <|-- Restriction
      
      Restriction : allValuesFrom
        
      Restriction : cardinality
        
      Restriction : complementOf
        
      Restriction : disjointWith
        
      Restriction : equivalentClass
        
          Restriction --> ClassExpression : equivalentClass
        
      Restriction : intersectionOf
        
          Restriction --> ClassExpression : intersectionOf
        
      Restriction : oneOf
        
          Restriction --> ClassExpression : oneOf
        
      Restriction : onProperty
        
          Restriction --> PropertyExpression : onProperty
        
      Restriction : someValuesFrom
        
      Restriction : subClassOf
        
          Restriction --> ClassExpression : subClassOf
        
      Restriction : unionOf
        
      
```





## Inheritance
* [Anonymous](Anonymous.md)
    * [AnonymousClassExpression](AnonymousClassExpression.md)
        * **Restriction** [ [ClassExpression](ClassExpression.md)]



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [onProperty](onProperty.md) | 0..* <br/> [PropertyExpression](PropertyExpression.md) |  | direct |
| [someValuesFrom](someValuesFrom.md) | 0..* <br/> [String](String.md) |  | direct |
| [allValuesFrom](allValuesFrom.md) | 0..1 <br/> [String](String.md) |  | direct |
| [disjointWith](disjointWith.md) | 0..* <br/> [String](String.md) |  | [ClassExpression](ClassExpression.md) |
| [equivalentClass](equivalentClass.md) | 0..* <br/> [ClassExpression](ClassExpression.md) |  | [ClassExpression](ClassExpression.md) |
| [intersectionOf](intersectionOf.md) | 0..1 <br/> [ClassExpression](ClassExpression.md) |  | [ClassExpression](ClassExpression.md) |
| [subClassOf](subClassOf.md) | 0..* <br/> [ClassExpression](ClassExpression.md) |  | [ClassExpression](ClassExpression.md) |
| [cardinality](cardinality.md) | 0..1 <br/> [String](String.md) |  | [ClassExpression](ClassExpression.md) |
| [complementOf](complementOf.md) | 0..1 <br/> [String](String.md) |  | [ClassExpression](ClassExpression.md) |
| [oneOf](oneOf.md) | 0..1 <br/> [ClassExpression](ClassExpression.md) |  | [ClassExpression](ClassExpression.md) |
| [unionOf](unionOf.md) | 0..1 <br/> [String](String.md) |  | [ClassExpression](ClassExpression.md) |



## Mixin Usage

| mixed into | description |
| --- | --- |








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/ontology-metadata





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | owl:Restriction |
| native | omoschema:Restriction |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Restriction
from_schema: https://w3id.org/oak/ontology-metadata
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
from_schema: https://w3id.org/oak/ontology-metadata
is_a: AnonymousClassExpression
mixin: true
mixins:
- ClassExpression
attributes:
  onProperty:
    name: onProperty
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:onProperty
    multivalued: true
    alias: onProperty
    owner: Restriction
    domain_of:
    - Restriction
    range: PropertyExpression
  someValuesFrom:
    name: someValuesFrom
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:someValuesFrom
    multivalued: true
    alias: someValuesFrom
    owner: Restriction
    domain_of:
    - Restriction
    range: string
  allValuesFrom:
    name: allValuesFrom
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:allValuesFrom
    alias: allValuesFrom
    owner: Restriction
    domain_of:
    - Restriction
    range: string
  disjointWith:
    name: disjointWith
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:disjointWith
    multivalued: true
    alias: disjointWith
    owner: Restriction
    domain_of:
    - ClassExpression
    - PropertyExpression
    range: string
  equivalentClass:
    name: equivalentClass
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    mixins:
    - match_aspect
    slot_uri: owl:equivalentClass
    multivalued: true
    alias: equivalentClass
    owner: Restriction
    domain_of:
    - ClassExpression
    range: ClassExpression
  intersectionOf:
    name: intersectionOf
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:intersectionOf
    alias: intersectionOf
    owner: Restriction
    domain_of:
    - ClassExpression
    range: ClassExpression
  subClassOf:
    name: subClassOf
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:subClassOf
    multivalued: true
    alias: subClassOf
    owner: Restriction
    domain_of:
    - ClassExpression
    range: ClassExpression
  cardinality:
    name: cardinality
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:cardinality
    alias: cardinality
    owner: Restriction
    domain_of:
    - ClassExpression
    range: string
  complementOf:
    name: complementOf
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:complementOf
    alias: complementOf
    owner: Restriction
    domain_of:
    - ClassExpression
    range: string
  oneOf:
    name: oneOf
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:oneOf
    alias: oneOf
    owner: Restriction
    domain_of:
    - ClassExpression
    range: ClassExpression
  unionOf:
    name: unionOf
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: owl:unionOf
    alias: unionOf
    owner: Restriction
    domain_of:
    - ClassExpression
    range: string
class_uri: owl:Restriction

```
</details>