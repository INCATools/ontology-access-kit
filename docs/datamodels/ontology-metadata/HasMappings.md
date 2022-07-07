# Class: HasMappings



* __NOTE__: this is a mixin class intended to be used in combination with other classes, and not used directly


URI: [omoschema:HasMappings](http://purl.obolibrary.org/obo/schema/HasMappings)




```{mermaid}
 classDiagram
      AnnotationPropertyMixin <|-- HasMappings
      
      HasMappings : broadMatch
      HasMappings : closeMatch
      HasMappings : database_cross_reference
      HasMappings : exactMatch
      HasMappings : narrowMatch
      

```





## Inheritance
* [AnnotationPropertyMixin](AnnotationPropertyMixin.md)
    * **HasMappings**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [broadMatch](broadMatch.md) | [Thing](Thing.md) | 0..* | None  | . |
| [closeMatch](closeMatch.md) | [Thing](Thing.md) | 0..* | None  | . |
| [exactMatch](exactMatch.md) | [Thing](Thing.md) | 0..* | None  | . |
| [narrowMatch](narrowMatch.md) | [Thing](Thing.md) | 0..* | None  | . |
| [database_cross_reference](database_cross_reference.md) | [CURIELiteral](CURIELiteral.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: http://purl.obolibrary.org/obo/omo/schema







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['omoschema:HasMappings'] |
| native | ['omoschema:HasMappings'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: HasMappings
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnnotationPropertyMixin
mixin: true
slots:
- broadMatch
- closeMatch
- exactMatch
- narrowMatch
- database_cross_reference

```
</details>

### Induced

<details>
```yaml
name: HasMappings
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: AnnotationPropertyMixin
mixin: true
attributes:
  broadMatch:
    name: broadMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:broadMatch
    multivalued: true
    alias: broadMatch
    owner: HasMappings
    range: Thing
  closeMatch:
    name: closeMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:closeMatch
    multivalued: true
    alias: closeMatch
    owner: HasMappings
    range: Thing
  exactMatch:
    name: exactMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:exactMatch
    multivalued: true
    alias: exactMatch
    owner: HasMappings
    range: Thing
  narrowMatch:
    name: narrowMatch
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: skos:narrowMatch
    multivalued: true
    alias: narrowMatch
    owner: HasMappings
    range: Thing
  database_cross_reference:
    name: database_cross_reference
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: match
    slot_uri: oio:hasDbXref
    multivalued: true
    alias: database_cross_reference
    owner: HasMappings
    range: CURIELiteral

```
</details>