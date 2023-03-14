# Validation Results Datamodel

A datamodel for data validation results.

URI: https://w3id.org/linkml/validation_results
Name: validaton-results



## Classes

| Class | Description |
| --- | --- |
| [ConstraintComponent](ConstraintComponent.md) |  |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external ... |
| [NamedResource](NamedResource.md) |  |
| [Node](Node.md) |  |
| [RepairConfiguration](RepairConfiguration.md) | Configuration parameters for execution of validation repairs |
| [RepairOperation](RepairOperation.md) | The result of performing an individual repair |
| [RepairReport](RepairReport.md) | A report that consists of repair operation results |
| [Report](Report.md) | A report object that is a holder to multiple report results |
| [Result](Result.md) | Abstract base class for any individual report result |
| [TypeSeverityKeyValue](TypeSeverityKeyValue.md) | key-value pair that maps a validation result type to a severity setting, for ... |
| [ValidationConfiguration](ValidationConfiguration.md) | Configuration parameters for execution of a validation report |
| [ValidationReport](ValidationReport.md) | A report that consists of validation results |
| [ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a parti... |


## Slots

| Slot | Description |
| --- | --- |
| [dry_run](dry_run.md) |  |
| [http_response_code](http_response_code.md) |  |
| [id](id.md) |  |
| [info](info.md) | additional information about the issue |
| [instantiates](instantiates.md) | The type of the subject |
| [max_number_results_per_type](max_number_results_per_type.md) | if set then truncate results such that no more than this number of results ar... |
| [modified](modified.md) |  |
| [number_of_attempts](number_of_attempts.md) |  |
| [object](object.md) |  |
| [object_str](object_str.md) |  |
| [predicate](predicate.md) | The predicate or property of the subject which the result is about |
| [repairs](repairs.md) |  |
| [results](results.md) | collection of results |
| [schema_path](schema_path.md) | allows overriding the default OMO schema |
| [severity](severity.md) | the severity of the issue |
| [source](source.md) |  |
| [subject](subject.md) | The instance which the result is about |
| [successful](successful.md) |  |
| [time_checked](time_checked.md) |  |
| [type](type.md) | The type of validation result |
| [type_severity_map](type_severity_map.md) | Allows overriding of severity of a particular type |
| [url](url.md) |  |
| [validation_configuration](validation_configuration.md) | repair configurations include validation configurations |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [SeverityOptions](SeverityOptions.md) |  |
| [ValidationResultType](ValidationResultType.md) |  |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
