# Slot: equivalentClass

URI: [owl:equivalentClass](http://www.w3.org/2002/07/owl#equivalentClass)




## Inheritance

* [logical_predicate](logical_predicate.md)
    * **equivalentClass** [ [match_aspect](match_aspect.md)]





## Applicable Classes

| Name | Description |
| --- | --- |
[ClassExpression](ClassExpression.md) | 
[Class](Class.md) | 
[Restriction](Restriction.md) | 






## Properties

* Range: [ClassExpression](ClassExpression.md)
* Multivalued: True








## TODOs

* restrict range

## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema




## LinkML Source

<details>
```yaml
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
domain_of:
- ClassExpression
range: ClassExpression

```
</details>