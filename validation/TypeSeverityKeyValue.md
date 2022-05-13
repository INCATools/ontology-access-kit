# Class: TypeSeverityKeyValue




URI: [reporting:TypeSeverityKeyValue](https://w3id.org/linkml/validation-model/TypeSeverityKeyValue)



<!-- no inheritance hierarchy -->



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [type](type.md) | [nodeidentifier](nodeidentifier.md) | 0..1 | None  | . |
| [severity](severity.md) | [SeverityOptions](SeverityOptions.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ValidationConfiguration](ValidationConfiguration.md) | [type_severity_map](type_severity_map.md) | range | TypeSeverityKeyValue |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TypeSeverityKeyValue
from_schema: https://w3id.org/linkml/validation_results
attributes:
  type:
    name: type
    from_schema: https://w3id.org/linkml/validation_results
    key: true
    range: nodeidentifier
  severity:
    name: severity
    from_schema: https://w3id.org/linkml/validation_results
    range: severity_options

```
</details>

### Induced

<details>
```yaml
name: TypeSeverityKeyValue
from_schema: https://w3id.org/linkml/validation_results
attributes:
  type:
    name: type
    from_schema: https://w3id.org/linkml/validation_results
    key: true
    alias: type
    owner: TypeSeverityKeyValue
    range: nodeidentifier
  severity:
    name: severity
    from_schema: https://w3id.org/linkml/validation_results
    alias: severity
    owner: TypeSeverityKeyValue
    range: severity_options

```
</details>