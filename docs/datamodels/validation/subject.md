# Slot: subject
_The instance which the result is about_


URI: [sh:focusNode](http://www.w3.org/ns/shacl#focusNode)



<!-- no inheritance hierarchy -->




## Applicable Classes

| Name | Description |
| --- | --- |
[ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a parti...
[ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external ...






## Properties

* Range: [Node](Node.md)
* Required: True








## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## LinkML Source

<details>
```yaml
name: subject
description: The instance which the result is about
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
slot_uri: sh:focusNode
alias: subject
domain_of:
- ValidationResult
range: Node
required: true

```
</details>