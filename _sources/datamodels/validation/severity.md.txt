

# Slot: severity


_the severity of the issue_





URI: [sh:resultSeverity](http://www.w3.org/ns/shacl#resultSeverity)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a parti... |  no  |
| [DefinitionValidationResult](DefinitionValidationResult.md) |  |  no  |
| [TypeSeverityKeyValue](TypeSeverityKeyValue.md) | key-value pair that maps a validation result type to a severity setting, for ... |  no  |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external ... |  no  |







## Properties

* Range: [SeverityOptions](SeverityOptions.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:resultSeverity |
| native | vm:severity |




## LinkML Source

<details>
```yaml
name: severity
description: the severity of the issue
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
slot_uri: sh:resultSeverity
alias: severity
domain_of:
- TypeSeverityKeyValue
- ValidationResult
range: severity_options

```
</details>