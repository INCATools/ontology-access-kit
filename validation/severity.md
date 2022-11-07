# Slot: severity
_the severity of the issue_


URI: [sh:resultSeverity](http://www.w3.org/ns/shacl#resultSeverity)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a particular rule
[TypeSeverityKeyValue](TypeSeverityKeyValue.md) | key-value pair that maps a validation result type to a severity setting, for overriding default severity
[ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external resource is still valid






## Properties

* Range: [SeverityOptions](SeverityOptions.md)






## Alias




## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




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