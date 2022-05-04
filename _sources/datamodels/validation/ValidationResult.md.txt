# Class: ValidationResult
_An individual result arising from validation of a data instance using a particular rule_





URI: [sh:ValidationResult](http://www.w3.org/ns/shacl#ValidationResult)




## Inheritance

* **ValidationResult**
    * [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md)




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [type](type.md) | [nodeidentifier](nodeidentifier.md) | 0..1 | The type of validation result. SHACL validation vocabulary is recommended for checks against a datamodel. For principle checks use the corresponding rule or principle, e.g. GO RULE ID, OBO Principle ID  | . |
| [severity](severity.md) | [SeverityOptions](SeverityOptions.md) | 0..1 | None  | . |
| [subject](subject.md) | [nodeidentifier](nodeidentifier.md) | 0..1 | None  | . |
| [instantiates](instantiates.md) | [nodeidentifier](nodeidentifier.md) | 0..1 | None  | . |
| [predicate](predicate.md) | [nodeidentifier](nodeidentifier.md) | 0..1 | None  | . |
| [object](object.md) | [nodeidentifier](nodeidentifier.md) | 0..1 | None  | . |
| [object_str](object_str.md) | [string](string.md) | 0..1 | None  | . |
| [source](source.md) | [nodeidentifier](nodeidentifier.md) | 0..1 | None  | . |
| [info](info.md) | [string](string.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ValidationReport](ValidationReport.md) | [results](results.md) | range | ValidationResult |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ValidationResult
description: An individual result arising from validation of a data instance using
  a particular rule
from_schema: https://w3id.org/linkml/validation_results
slots:
- type
- severity
- subject
- instantiates
- predicate
- object
- object_str
- source
- info
class_uri: sh:ValidationResult

```
</details>

### Induced

<details>
```yaml
name: ValidationResult
description: An individual result arising from validation of a data instance using
  a particular rule
from_schema: https://w3id.org/linkml/validation_results
attributes:
  type:
    name: type
    description: The type of validation result. SHACL validation vocabulary is recommended
      for checks against a datamodel. For principle checks use the corresponding rule
      or principle, e.g. GO RULE ID, OBO Principle ID
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:sourceConstraintComponent
    alias: type
    owner: ValidationResult
    range: nodeidentifier
  severity:
    name: severity
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:resultSeverity
    alias: severity
    owner: ValidationResult
    range: severity_options
  subject:
    name: subject
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:focusNode
    alias: subject
    owner: ValidationResult
    range: nodeidentifier
  instantiates:
    name: instantiates
    exact_mappings:
    - sh:sourceShape
    from_schema: https://w3id.org/linkml/validation_results
    alias: instantiates
    owner: ValidationResult
    range: nodeidentifier
  predicate:
    name: predicate
    related_mappings:
    - sh:resultPath
    from_schema: https://w3id.org/linkml/validation_results
    alias: predicate
    owner: ValidationResult
    range: nodeidentifier
  object:
    name: object
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:value
    alias: object
    owner: ValidationResult
    range: nodeidentifier
  object_str:
    name: object_str
    from_schema: https://w3id.org/linkml/validation_results
    alias: object_str
    owner: ValidationResult
    range: string
  source:
    name: source
    from_schema: https://w3id.org/linkml/validation_results
    alias: source
    owner: ValidationResult
    range: nodeidentifier
  info:
    name: info
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:resultMessage
    alias: info
    owner: ValidationResult
    range: string
class_uri: sh:ValidationResult

```
</details>