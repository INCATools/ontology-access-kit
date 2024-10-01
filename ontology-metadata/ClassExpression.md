

# Class: ClassExpression



URI: [omoschema:ClassExpression](https://w3id.org/oak/ontology-metadata/ClassExpression)






```{mermaid}
 classDiagram
    class ClassExpression
    click ClassExpression href "../ClassExpression"
      Expression <|-- ClassExpression
        click Expression href "../Expression"
      

      ClassExpression <|-- Class
        click Class href "../Class"
      ClassExpression <|-- Restriction
        click Restriction href "../Restriction"
      
      
      ClassExpression : cardinality
        
      ClassExpression : complementOf
        
      ClassExpression : disjointWith
        
      ClassExpression : equivalentClass
        
          
    
    
    ClassExpression --> "*" ClassExpression : equivalentClass
    click ClassExpression href "../ClassExpression"

        
      ClassExpression : intersectionOf
        
          
    
    
    ClassExpression --> "0..1" ClassExpression : intersectionOf
    click ClassExpression href "../ClassExpression"

        
      ClassExpression : oneOf
        
          
    
    
    ClassExpression --> "0..1" ClassExpression : oneOf
    click ClassExpression href "../ClassExpression"

        
      ClassExpression : subClassOf
        
          
    
    
    ClassExpression --> "*" ClassExpression : subClassOf
    click ClassExpression href "../ClassExpression"

        
      ClassExpression : unionOf
        
      
```





## Inheritance
* [Expression](Expression.md)
    * **ClassExpression**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [disjointWith](disjointWith.md) | * <br/> [String](String.md) |  | direct |
| [equivalentClass](equivalentClass.md) | * <br/> [ClassExpression](ClassExpression.md) |  | direct |
| [intersectionOf](intersectionOf.md) | 0..1 <br/> [ClassExpression](ClassExpression.md) |  | direct |
| [subClassOf](subClassOf.md) | * <br/> [ClassExpression](ClassExpression.md) |  | direct |
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


* from schema: https://w3id.org/oak/ontology-metadata




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
from_schema: https://w3id.org/oak/ontology-metadata
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
    owner: ClassExpression
    domain_of:
    - ClassExpression
    - PropertyExpression
    range: string
    multivalued: true
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
    alias: equivalentClass
    owner: ClassExpression
    domain_of:
    - ClassExpression
    range: ClassExpression
    multivalued: true
  intersectionOf:
    name: intersectionOf
    todos:
    - restrict range
    from_schema: https://w3id.org/oak/ontology-metadata
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
    from_schema: https://w3id.org/oak/ontology-metadata
    rank: 1000
    is_a: logical_predicate
    slot_uri: rdfs:subClassOf
    alias: subClassOf
    owner: ClassExpression
    domain_of:
    - ClassExpression
    range: ClassExpression
    multivalued: true
  cardinality:
    name: cardinality
    from_schema: https://w3id.org/oak/ontology-metadata
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
    from_schema: https://w3id.org/oak/ontology-metadata
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
    from_schema: https://w3id.org/oak/ontology-metadata
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
    from_schema: https://w3id.org/oak/ontology-metadata
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