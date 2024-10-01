# Validation Results Data Model

A datamodel for data validation results.

URI: https://w3id.org/linkml/validation_results

Name: validaton-results



## Classes

| Class | Description |
| --- | --- |
| [NamedResource](NamedResource.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ConstraintComponent](ConstraintComponent.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Node](Node.md) | None |
| [RepairConfiguration](RepairConfiguration.md) | Configuration parameters for execution of validation repairs |
| [Report](Report.md) | A report object that is a holder to multiple report results |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[RepairReport](RepairReport.md) | A report that consists of repair operation results |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ValidationReport](ValidationReport.md) | A report that consists of validation results |
| [Result](Result.md) | Abstract base class for any individual report result |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MappingValidationResult](MappingValidationResult.md) | A validation result where the check is to determine if a mapping is correct |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[RepairOperation](RepairOperation.md) | The result of performing an individual repair |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ValidationResult](ValidationResult.md) | An individual result arising from validation of a data instance using a particular rule |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DefinitionValidationResult](DefinitionValidationResult.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ExternalReferenceValidationResult](ExternalReferenceValidationResult.md) | A validation result where the check is to determine if a link to an external resource is still valid |
| [TypeSeverityKeyValue](TypeSeverityKeyValue.md) | key-value pair that maps a validation result type to a severity setting, for overriding default severity |
| [ValidationConfiguration](ValidationConfiguration.md) | Configuration parameters for execution of a validation report |



## Slots

| Slot | Description |
| --- | --- |
| [category](category.md) | The category of the validation issue |
| [confidence](confidence.md) |  |
| [definition](definition.md) |  |
| [definition_source](definition_source.md) |  |
| [documentation_objects](documentation_objects.md) | paths or URLs to files containing best practice documentation, SOPs, etc |
| [dry_run](dry_run.md) |  |
| [http_response_code](http_response_code.md) |  |
| [id](id.md) |  |
| [info](info.md) | additional information about the issue |
| [instantiates](instantiates.md) | The type of the subject |
| [lookup_references](lookup_references.md) | if true, then look up references used as provenance (axiom annotation) |
| [max_number_results_per_type](max_number_results_per_type.md) | if set then truncate results such that no more than this number of results ar... |
| [modified](modified.md) |  |
| [number_of_attempts](number_of_attempts.md) |  |
| [object](object.md) |  |
| [object_id](object_id.md) |  |
| [object_info](object_info.md) |  |
| [object_str](object_str.md) |  |
| [predicate](predicate.md) | The predicate or property of the subject which the result is about |
| [predicate_id](predicate_id.md) |  |
| [problem](problem.md) |  |
| [prompt_info](prompt_info.md) | for AI agents, this allows passing through of additional info to the prompt |
| [proposed_new_definition](proposed_new_definition.md) |  |
| [repairs](repairs.md) |  |
| [results](results.md) | collection of results |
| [schema_path](schema_path.md) | allows overriding the default OMO schema |
| [severity](severity.md) | the severity of the issue |
| [source](source.md) |  |
| [subject](subject.md) | The instance which the result is about |
| [subject_id](subject_id.md) |  |
| [subject_info](subject_info.md) |  |
| [successful](successful.md) |  |
| [suggested_modifications](suggested_modifications.md) |  |
| [suggested_predicate](suggested_predicate.md) |  |
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
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
