# Class: ValidationConfiguration
_Configuration parameters for execution of a validation report_




URI: [vm:ValidationConfiguration](https://w3id.org/linkml/validation-model/ValidationConfiguration)



```{mermaid}
 classDiagram
    class ValidationConfiguration
      ValidationConfiguration : max_number_results_per_type
        
      ValidationConfiguration : schema_path
        
      ValidationConfiguration : type_severity_map
        
          ValidationConfiguration ..> TypeSeverityKeyValue : type_severity_map
        
      
```




<!-- no inheritance hierarchy -->


## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [max_number_results_per_type](max_number_results_per_type.md) | 0..1 <br/> [Integer](Integer.md) | if set then truncate results such that no more than this number of results ar... | direct |
| [type_severity_map](type_severity_map.md) | 0..* <br/> [TypeSeverityKeyValue](TypeSeverityKeyValue.md) | Allows overriding of severity of a particular type | direct |
| [schema_path](schema_path.md) | 0..1 <br/> [String](String.md) | allows overriding the default OMO schema | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [RepairConfiguration](RepairConfiguration.md) | [validation_configuration](validation_configuration.md) | range | [ValidationConfiguration](ValidationConfiguration.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:ValidationConfiguration |
| native | vm:ValidationConfiguration |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ValidationConfiguration
description: Configuration parameters for execution of a validation report
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
attributes:
  max_number_results_per_type:
    name: max_number_results_per_type
    description: if set then truncate results such that no more than this number of
      results are reported per type
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    range: integer
  type_severity_map:
    name: type_severity_map
    description: Allows overriding of severity of a particular type
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    multivalued: true
    range: TypeSeverityKeyValue
    inlined: true
  schema_path:
    name: schema_path
    description: allows overriding the default OMO schema
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    range: string

```
</details>

### Induced

<details>
```yaml
name: ValidationConfiguration
description: Configuration parameters for execution of a validation report
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
attributes:
  max_number_results_per_type:
    name: max_number_results_per_type
    description: if set then truncate results such that no more than this number of
      results are reported per type
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: max_number_results_per_type
    owner: ValidationConfiguration
    domain_of:
    - ValidationConfiguration
    range: integer
  type_severity_map:
    name: type_severity_map
    description: Allows overriding of severity of a particular type
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    multivalued: true
    alias: type_severity_map
    owner: ValidationConfiguration
    domain_of:
    - ValidationConfiguration
    range: TypeSeverityKeyValue
    inlined: true
  schema_path:
    name: schema_path
    description: allows overriding the default OMO schema
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: schema_path
    owner: ValidationConfiguration
    domain_of:
    - ValidationConfiguration
    range: string

```
</details>