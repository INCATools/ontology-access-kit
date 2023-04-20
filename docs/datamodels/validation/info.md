# Slot: info
_additional information about the issue_


URI: [sh:resultMessage](http://www.w3.org/ns/shacl#resultMessage)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a parti...
[RepairOperation](RepairOperation.md) | The result of performing an individual repair
[ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external ...






## Properties

* Range: [String](String.md)







## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## LinkML Source

<details>
```yaml
name: info
description: additional information about the issue
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
slot_uri: sh:resultMessage
alias: info
domain_of:
- ValidationResult
- RepairOperation
range: string

```
</details>