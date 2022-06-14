# Validation Results Datamodel

A datamodel for data validation results.

URI: https://w3id.org/linkml/validation_results
Name: validaton-results

## Classes

| Class | Description |
| --- | --- |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external resource is still valid |
| [RepairConfiguration](RepairConfiguration.md) | Configuration parameters for execution of validation repairs |
| [RepairOperation](RepairOperation.md) | The result of performing an individual repair |
| [RepairReport](RepairReport.md) | A report that consists of repair operation results |
| [Report](Report.md) | A report object that is a holder to multiple report results |
| [Result](Result.md) | Abstract base class for any individual report result |
| [TypeSeverityKeyValue](TypeSeverityKeyValue.md) | key-value pair that maps a validation result type to a severity setting, for overriding default severity |
| [ValidationConfiguration](ValidationConfiguration.md) | Configuration parameters for execution of a validation report |
| [ValidationReport](ValidationReport.md) | A report that consists of validation results |
| [ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a particular rule |


## Slots

| Slot | Description |
| --- | --- |
| [dry_run](dry_run.md) | None |
| [http_response_code](http_response_code.md) | None |
| [info](info.md) | additional information about the issue |
| [instantiates](instantiates.md) | The type of the subject |
| [max_number_results_per_type](max_number_results_per_type.md) | if set then truncate results such that no more than this number of results are reported per type |
| [modified](modified.md) | None |
| [number_of_attempts](number_of_attempts.md) | None |
| [object](object.md) | None |
| [object_str](object_str.md) | None |
| [predicate](predicate.md) | The predicate or property of the subject which the result is about |
| [repairs](repairs.md) | None |
| [results](results.md) | collection of results |
| [schema_path](schema_path.md) | allows overriding the default OMO schema |
| [severity](severity.md) | the severity of the issue |
| [source](source.md) | None |
| [subject](subject.md) | The instance which the result is about |
| [successful](successful.md) | None |
| [time_checked](time_checked.md) | None |
| [type](type.md) | The type of validation result. SHACL validation vocabulary is recommended for checks against a datamodel. For principle checks use the corresponding rule or principle, e.g. GO RULE ID, OBO Principle ID |
| [type_severity_map](type_severity_map.md) | Allows overriding of severity of a particular type |
| [url](url.md) | None |
| [validation_configuration](validation_configuration.md) | repair configurations include validation configurations |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [SeverityOptions](SeverityOptions.md) | None |
| [ValidationResultType](ValidationResultType.md) | None |


## Subsets

| Subset | Description |
| --- | --- |
