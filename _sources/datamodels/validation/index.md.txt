# Validation Results Datamodel

A datamodel for data validation results.

URI: https://w3id.org/linkml/validation_results
Name: validaton-results

## Classes

| Class | Description |
| --- | --- |
| [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external ... |
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
| [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | A binary (true or false) value |
| [xsd:date](http://www.w3.org/2001/XMLSchema#date) | a date (year, month and day) in an idealized calendar |
| [linkml:DateOrDatetime](https://w3id.org/linkml/DateOrDatetime) | Either a date or a datetime |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | The combination of a date and time |
| [xsd:decimal](http://www.w3.org/2001/XMLSchema#decimal) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [xsd:double](http://www.w3.org/2001/XMLSchema#double) | A real number that conforms to the xsd:double specification |
| [xsd:float](http://www.w3.org/2001/XMLSchema#float) | A real number that conforms to the xsd:float specification |
| [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | An integer |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | Prefix part of CURIE |
| [shex:nonLiteral](shex:nonLiteral) | A URI, CURIE or BNODE that represents a node in a model |
| [shex:iri](shex:iri) | A URI or CURIE that represents an object in the model |
| [xsd:string](http://www.w3.org/2001/XMLSchema#string) | A character string |
| [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) | A time object represents a (local) time of day, independent of any particular... |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a complete URI |
| [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
