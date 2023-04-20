# Class: Precondition
_A pattern to be matched against an individual SSSOM mapping_




URI: [mappingrules:Precondition](https://w3id.org/oak/mapping-rules-datamodel/Precondition)



```{mermaid}
 classDiagram
    class Precondition
      Precondition : mapping_source_one_of
        
      Precondition : object_match_field_one_of
        
      Precondition : object_source_one_of
        
      Precondition : predicate_id_one_of
        
      Precondition : subject_match_field_one_of
        
      Precondition : subject_source_one_of
        
      Precondition : transformations_included_in
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject_source_one_of](subject_source_one_of.md) | 0..* <br/> [String](String.md) |  | direct |
| [object_source_one_of](object_source_one_of.md) | 0..* <br/> [String](String.md) |  | direct |
| [mapping_source_one_of](mapping_source_one_of.md) | 0..* <br/> [String](String.md) |  | direct |
| [subject_match_field_one_of](subject_match_field_one_of.md) | 0..* <br/> [String](String.md) |  | direct |
| [object_match_field_one_of](object_match_field_one_of.md) | 0..* <br/> [String](String.md) |  | direct |
| [transformations_included_in](transformations_included_in.md) | 0..* <br/> [String](String.md) |  | direct |
| [predicate_id_one_of](predicate_id_one_of.md) | 0..* <br/> [String](String.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [MappingRule](MappingRule.md) | [preconditions](preconditions.md) | range | [Precondition](Precondition.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:Precondition |
| native | mappingrules:Precondition |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Precondition
description: A pattern to be matched against an individual SSSOM mapping
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
attributes:
  subject_source_one_of:
    name: subject_source_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
  object_source_one_of:
    name: object_source_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
  mapping_source_one_of:
    name: mapping_source_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
  subject_match_field_one_of:
    name: subject_match_field_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
  object_match_field_one_of:
    name: object_match_field_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
  transformations_included_in:
    name: transformations_included_in
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
  predicate_id_one_of:
    name: predicate_id_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true

```
</details>

### Induced

<details>
```yaml
name: Precondition
description: A pattern to be matched against an individual SSSOM mapping
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
attributes:
  subject_source_one_of:
    name: subject_source_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
    alias: subject_source_one_of
    owner: Precondition
    domain_of:
    - Precondition
    range: string
  object_source_one_of:
    name: object_source_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
    alias: object_source_one_of
    owner: Precondition
    domain_of:
    - Precondition
    range: string
  mapping_source_one_of:
    name: mapping_source_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
    alias: mapping_source_one_of
    owner: Precondition
    domain_of:
    - Precondition
    range: string
  subject_match_field_one_of:
    name: subject_match_field_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
    alias: subject_match_field_one_of
    owner: Precondition
    domain_of:
    - Precondition
    range: string
  object_match_field_one_of:
    name: object_match_field_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
    alias: object_match_field_one_of
    owner: Precondition
    domain_of:
    - Precondition
    range: string
  transformations_included_in:
    name: transformations_included_in
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
    alias: transformations_included_in
    owner: Precondition
    domain_of:
    - Precondition
    range: string
  predicate_id_one_of:
    name: predicate_id_one_of
    from_schema: https://w3id.org/oak/mapping-rules-datamodel
    rank: 1000
    multivalued: true
    alias: predicate_id_one_of
    owner: Precondition
    domain_of:
    - Precondition
    range: string

```
</details>