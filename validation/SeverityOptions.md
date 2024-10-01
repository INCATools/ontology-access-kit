# Enum: SeverityOptions



URI: [SeverityOptions](SeverityOptions.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| FATAL | None |  |
| ERROR | sh:Violation |  |
| WARNING | sh:Warning |  |
| INFO | sh:Info |  |




## Slots

| Name | Description |
| ---  | --- |
| [severity](severity.md) | the severity of the issue |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results






## LinkML Source

<details>
```yaml
name: severity_options
from_schema: https://w3id.org/linkml/validation_results
exact_mappings:
- sh:Severity
rank: 1000
permissible_values:
  FATAL:
    text: FATAL
  ERROR:
    text: ERROR
    meaning: sh:Violation
  WARNING:
    text: WARNING
    meaning: sh:Warning
  INFO:
    text: INFO
    meaning: sh:Info

```
</details>
