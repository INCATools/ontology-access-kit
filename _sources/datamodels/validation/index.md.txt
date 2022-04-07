# validaton-results

A datamodel for reports on data

URI: https://w3id.org/linkml/validation_results

## Classes

| Class | Description |
| --- | --- |
| [ValidationReport](ValidationReport.md) | A report object | 
| [ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a particular rule | 
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external resource is still valid | 


## Slots

| Slot | Description |
| --- | --- |
| [type](type.md) | The type of validation result. SHACL validation vocabulary is recommended for checks against a datamodel. For principle checks use the corresponding rule or principle, e.g. GO RULE ID, OBO Principle ID | 
| [subject](subject.md) | None | 
| [instantiates](instantiates.md) | None | 
| [predicate](predicate.md) | None | 
| [object](object.md) | None | 
| [object_str](object_str.md) | None | 
| [source](source.md) | None | 
| [severity](severity.md) | None | 
| [info](info.md) | None | 
| [results](results.md) | None | 
| [url](url.md) | None | 
| [time_checked](time_checked.md) | None | 
| [number_of_attempts](number_of_attempts.md) | None | 
| [http_response_code](http_response_code.md) | None | 


## Enums

| Enums | Description |
| --- | --- |
| [SeverityOptions](SeverityOptions.md) | None | 

