# Class: ValidationConfiguration
_Configuration parameters for execution of a validation report_





URI: [reporting:ValidationConfiguration](https://w3id.org/linkml/validation-model/ValidationConfiguration)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [max_number_results_per_type](max_number_results_per_type.md) | [integer](integer.md) | 0..1 | if set then truncate results such that no more than this number of results are reported per type  | . |
| [type_severity_map](type_severity_map.md) | [TypeSeverityKeyValue](TypeSeverityKeyValue.md) | 0..* | Allows overriding of severity of a particular type  | . |
| [schema_path](schema_path.md) | [string](string.md) | 0..1 | allows overriding the default OMO schema  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [RepairConfiguration](RepairConfiguration.md) | [validation_configuration](validation_configuration.md) | range | ValidationConfiguration |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ValidationConfiguration
description: Configuration parameters for execution of a validation report
from_schema: https://w3id.org/linkml/validation_results
attributes:
  max_number_results_per_type:
    name: max_number_results_per_type
    description: if set then truncate results such that no more than this number of
      results are reported per type
    from_schema: https://w3id.org/linkml/validation_results
    range: integer
  type_severity_map:
    name: type_severity_map
    description: Allows overriding of severity of a particular type
    from_schema: https://w3id.org/linkml/validation_results
    multivalued: true
    inlined: true
    range: TypeSeverityKeyValue
  schema_path:
    name: schema_path
    description: allows overriding the default OMO schema
    from_schema: https://w3id.org/linkml/validation_results
    range: string

```
</details>

### Induced

<details>
```yaml
name: ValidationConfiguration
description: Configuration parameters for execution of a validation report
from_schema: https://w3id.org/linkml/validation_results
attributes:
  max_number_results_per_type:
    name: max_number_results_per_type
    description: if set then truncate results such that no more than this number of
      results are reported per type
    from_schema: https://w3id.org/linkml/validation_results
    alias: max_number_results_per_type
    owner: ValidationConfiguration
    range: integer
  type_severity_map:
    name: type_severity_map
    description: Allows overriding of severity of a particular type
    from_schema: https://w3id.org/linkml/validation_results
    multivalued: true
    inlined: true
    alias: type_severity_map
    owner: ValidationConfiguration
    range: TypeSeverityKeyValue
  schema_path:
    name: schema_path
    description: allows overriding the default OMO schema
    from_schema: https://w3id.org/linkml/validation_results
    alias: schema_path
    owner: ValidationConfiguration
    range: string

```
</details>