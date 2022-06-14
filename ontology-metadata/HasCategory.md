# Class: HasCategory



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:HasCategory](http://purl.obolibrary.org/obo/schema/HasCategory)




```{mermaid}
 classDiagram
      AnnotationPropertyMixin <|-- HasCategory
      
      HasCategory : category
      HasCategory : conformsTo
      HasCategory : has_obo_namespace
      HasCategory : in_subset
      

```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasCategory**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [has_obo_namespace](has_obo_namespace.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [category](category.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [in_subset](in_subset.md) | [Subset](Subset.md) | 0..* | Maps an ontology element to a subset it belongs to  | . |
| [conformsTo](conformsTo.md) | [Thing](Thing.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['omoschema:HasCategory'] |
| native | ['omoschema:HasCategory'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasCategory
from_schema: http://purl.obolibrary.org/obo/omo/schema
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
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  has_obo_namespace:
    name: has_obo_namespace
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:hasOBONamespace
    multivalued: true
    alias: has_obo_namespace
    owner: HasCategory
    range: string
  category:
    name: category
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: biolink:category
    alias: category
    owner: HasCategory
    range: string
  in_subset:
    name: in_subset
    description: Maps an ontology element to a subset it belongs to
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    slot_uri: oio:inSubset
    multivalued: true
    alias: in_subset
    owner: HasCategory
    range: Subset
  conformsTo:
    name: conformsTo
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: informative_property
    slot_uri: dcterms:conformsTo
    multivalued: true
    alias: conformsTo
    owner: HasCategory
    range: Thing

```
</details>