

# Slot: type


_The type of validation result. SHACL validation vocabulary is recommended for checks against a datamodel. For principle checks use the corresponding rule or principle, e.g. GO RULE ID, OBO Principle ID_





URI: [sh:sourceConstraintComponent](http://www.w3.org/ns/shacl#sourceConstraintComponent)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a parti... |  no  |
| [DefinitionValidationResult](DefinitionValidationResult.md) |  |  no  |
| [TypeSeverityKeyValue](TypeSeverityKeyValue.md) | key-value pair that maps a validation result type to a severity setting, for ... |  no  |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external ... |  no  |







## Properties

* Range: [ConstraintComponent](ConstraintComponent.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:sourceConstraintComponent |
| native | vm:type |




## LinkML Source

<details>
```yaml
name: type
description: The type of validation result. SHACL validation vocabulary is recommended
  for checks against a datamodel. For principle checks use the corresponding rule
  or principle, e.g. GO RULE ID, OBO Principle ID
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
slot_uri: sh:sourceConstraintComponent
alias: type
domain_of:
- TypeSeverityKeyValue
- ValidationResult
range: ConstraintComponent
required: true

```
</details>