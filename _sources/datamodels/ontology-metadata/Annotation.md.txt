# Class: Annotation
_A reified property-object pair_




URI: [omoschema:Annotation](http://purl.obolibrary.org/obo/schema/Annotation)


```{mermaid}
 classDiagram
    class Annotation
      Annotation : object
      Annotation : predicate
      
```



<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [predicate](predicate.md) | 0..1 <br/> None | None | direct |
| [object](object.md) | 0..1 <br/> None | None | direct |



## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Axiom](Axiom.md) | [annotations](annotations.md) | range | Annotation |







## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:Annotation |
| native | omoschema:Annotation |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Annotation
description: A reified property-object pair
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
attributes:
  predicate:
    name: predicate
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    relational_role: PREDICATE
  object:
    name: object
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    relational_role: OBJECT
represents_relationship: true

```
</details>

### Induced

<details>
```yaml
name: Annotation
description: A reified property-object pair
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
attributes:
  predicate:
    name: predicate
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    alias: predicate
    owner: Annotation
    domain_of:
    - Annotation
    relational_role: PREDICATE
    range: string
  object:
    name: object
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    alias: object
    owner: Annotation
    domain_of:
    - Annotation
    relational_role: OBJECT
    range: string
represents_relationship: true

```
</details>