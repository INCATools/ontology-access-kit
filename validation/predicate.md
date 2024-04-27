

# Slot: predicate


_The predicate or property of the subject which the result is about_



URI: [vm:predicate](https://w3id.org/linkml/validation-model/predicate)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a parti... |  no  |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external ... |  no  |
| [DefinitionValidationResult](DefinitionValidationResult.md) |  |  no  |







## Properties

* Range: [Node](Node.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## LinkML Source

<details>
```yaml
name: predicate
description: The predicate or property of the subject which the result is about
from_schema: https://w3id.org/linkml/validation_results
related_mappings:
- sh:resultPath
rank: 1000
alias: predicate
domain_of:
- ValidationResult
range: Node

```
</details>