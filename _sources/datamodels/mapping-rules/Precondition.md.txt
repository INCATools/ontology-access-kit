# Class: Precondition
_A pattern to be matched against an individual SSSOM mapping_





URI: [mrules:Precondition](https://w3id.org/linkml/mapping_rules_datamodel/Precondition)




```{mermaid}
 classDiagram
    class Precondition
      Precondition : mapping_source_one_of
      Precondition : object_match_field_one_of
      Precondition : object_source_one_of
      Precondition : subject_match_field_one_of
      Precondition : subject_source_one_of
      Precondition : transformations_included_in
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [subject_source_one_of](subject_source_one_of.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [object_source_one_of](object_source_one_of.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [mapping_source_one_of](mapping_source_one_of.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [subject_match_field_one_of](subject_match_field_one_of.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [object_match_field_one_of](object_match_field_one_of.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |
| [transformations_included_in](transformations_included_in.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..* | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRule](MappingRule.md) | [preconditions](preconditions.md) | range | Precondition |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/mapping_rules_datamodel







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['mrules:Precondition'] |
| native | ['mrules:Precondition'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Precondition
description: A pattern to be matched against an individual SSSOM mapping
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
attributes:
  subject_source_one_of:
    name: subject_source_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
  object_source_one_of:
    name: object_source_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
  mapping_source_one_of:
    name: mapping_source_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
  subject_match_field_one_of:
    name: subject_match_field_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
  object_match_field_one_of:
    name: object_match_field_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
  transformations_included_in:
    name: transformations_included_in
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: Precondition
description: A pattern to be matched against an individual SSSOM mapping
from_schema: https://w3id.org/linkml/mapping_rules_datamodel
attributes:
  subject_source_one_of:
    name: subject_source_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
    alias: subject_source_one_of
    owner: Precondition
    range: string
  object_source_one_of:
    name: object_source_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
    alias: object_source_one_of
    owner: Precondition
    range: string
  mapping_source_one_of:
    name: mapping_source_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
    alias: mapping_source_one_of
    owner: Precondition
    range: string
  subject_match_field_one_of:
    name: subject_match_field_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
    alias: subject_match_field_one_of
    owner: Precondition
    range: string
  object_match_field_one_of:
    name: object_match_field_one_of
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
    alias: object_match_field_one_of
    owner: Precondition
    range: string
  transformations_included_in:
    name: transformations_included_in
    from_schema: https://w3id.org/linkml/mapping_rules_datamodel
    multivalued: true
    alias: transformations_included_in
    owner: Precondition
    range: string

```
</details>