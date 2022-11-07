# Slot: info
_additional information about the issue_


URI: [sh:resultMessage](http://www.w3.org/ns/shacl#resultMessage)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a particular rule
[RepairOperation](RepairOperation.md) | The result of performing an individual repair
[ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external resource is still valid






## Properties

* Range: [xsd:string](http://www.w3.org/2001/XMLSchema#string)






## Alias




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