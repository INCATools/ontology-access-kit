# Class: HasCategory



URI: [omoschema:HasCategory](http://purl.obolibrary.org/obo/schema/HasCategory)


```{mermaid}
 classDiagram
    class HasCategory
      AnnotationPropertyMixin <|-- HasCategory
      
      HasCategory : category
      HasCategory : conformsTo
      HasCategory : has_obo_namespace
      HasCategory : in_subset
      

      HasCategory <|-- Term
      
      HasCategory : category
      HasCategory : conformsTo
      HasCategory : has_obo_namespace
      HasCategory : in_subset
      
```




## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasCategory**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [has_obo_namespace](has_obo_namespace.md) | 0..* <br/> None | None | direct |
| [category](category.md) | 0..1 <br/> None | None | direct |
| [in_subset](in_subset.md) | 0..* <br/> Subset | Maps an ontology element to a subset it belongs to | direct |
| [conformsTo](conformsTo.md) | 0..* <br/> Thing | None | direct |

## Mixin Usage

| mixed into | description |
| --- | --- |
| [Term](Term.md) | A NamedThing that includes classes, properties, but not ontologies |









## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | omoschema:HasCategory |
| native | omoschema:HasCategory |


## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasCategory
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: AnnotationPropertyMixin
mixin: true
slots:
- has_obo_namespace
- category
- in_subset
- conformsTo

```
</details>

### Induced

<details>
```yaml
name: HasCategory
from_schema: http://purl.obolibrary.org/obo/omo/schema
rank: 1000
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  has_obo_namespace:
    name: has_obo_namespace
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:hasOBONamespace
    multivalued: true
    alias: has_obo_namespace
    owner: HasCategory
    domain_of:
    - HasCategory
    range: string
  category:
    name: category
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: biolink:category
    alias: category
    owner: HasCategory
    domain_of:
    - HasCategory
    range: string
  in_subset:
    name: in_subset
    description: Maps an ontology element to a subset it belongs to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    slot_uri: oio:inSubset
    multivalued: true
    alias: in_subset
    owner: HasCategory
    domain_of:
    - HasCategory
    range: Subset
  conformsTo:
    name: conformsTo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    rank: 1000
    is_a: informative_property
    slot_uri: dcterms:conformsTo
    multivalued: true
    alias: conformsTo
    owner: HasCategory
    domain_of:
    - HasCategory
    range: Thing

```
</details>