# Class: ValidationResult
_An individual result arising from validation of a data instance using a particular rule_





URI: [sh:ValidationResult](http://www.w3.org/ns/shacl#ValidationResult)




```{mermaid}
 classDiagram
      Result <|-- ValidationResult
      
      ValidationResult : info
      ValidationResult : instantiates
      ValidationResult : object
      ValidationResult : object_str
      ValidationResult : predicate
      ValidationResult : severity
      ValidationResult : source
      ValidationResult : subject
      ValidationResult : type
      

```





## Inheritance
* [Result](Result.md)
    * **ValidationResult**
        * [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md)



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [type](type.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 1..1 | The type of validation result. SHACL validation vocabulary is recommended for checks against a datamodel. For principle checks use the corresponding rule or principle, e.g. GO RULE ID, OBO Principle ID  | . |
| [severity](severity.md) | [SeverityOptions](SeverityOptions.md) | 0..1 | the severity of the issue  | . |
| [subject](subject.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 1..1 | The instance which the result is about  | . |
| [instantiates](instantiates.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..1 | The type of the subject  | . |
| [predicate](predicate.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..1 | The predicate or property of the subject which the result is about  | . |
| [object](object.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..1 | None  | . |
| [object_str](object_str.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [source](source.md) | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) | 0..1 | None  | . |
| [info](info.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | additional information about the issue  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ValidationReport](ValidationReport.md) | [results](results.md) | range | ValidationResult |
| [RepairOperation](RepairOperation.md) | [repairs](repairs.md) | range | ValidationResult |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['sh:ValidationResult'] |
| native | ['vm:ValidationResult'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ValidationResult
description: An individual result arising from validation of a data instance using
  a particular rule
from_schema: https://w3id.org/linkml/validation_results
is_a: Result
slots:
- type
- severity
- subject
- instantiates
- predicate
- object
- object_str
- source
- info
class_uri: sh:ValidationResult

```
</details>

### Induced

<details>
```yaml
name: ValidationResult
description: An individual result arising from validation of a data instance using
  a particular rule
from_schema: https://w3id.org/linkml/validation_results
is_a: Result
attributes:
  type:
    name: type
    description: The type of validation result. SHACL validation vocabulary is recommended
      for checks against a datamodel. For principle checks use the corresponding rule
      or principle, e.g. GO RULE ID, OBO Principle ID
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:sourceConstraintComponent
    alias: type
    owner: ValidationResult
    range: uriorcurie
    required: true
  severity:
    name: severity
    description: the severity of the issue
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:resultSeverity
    alias: severity
    owner: ValidationResult
    range: severity_options
  subject:
    name: subject
    description: The instance which the result is about
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:focusNode
    alias: subject
    owner: ValidationResult
    range: uriorcurie
    required: true
  instantiates:
    name: instantiates
    description: The type of the subject
    from_schema: https://w3id.org/linkml/validation_results
    exact_mappings:
    - sh:sourceShape
    alias: instantiates
    owner: ValidationResult
    range: uriorcurie
  predicate:
    name: predicate
    description: The predicate or property of the subject which the result is about
    from_schema: https://w3id.org/linkml/validation_results
    related_mappings:
    - sh:resultPath
    alias: predicate
    owner: ValidationResult
    range: uriorcurie
  object:
    name: object
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:value
    alias: object
    owner: ValidationResult
    range: uriorcurie
  object_str:
    name: object_str
    from_schema: https://w3id.org/linkml/validation_results
    alias: object_str
    owner: ValidationResult
    range: string
  source:
    name: source
    from_schema: https://w3id.org/linkml/validation_results
    alias: source
    owner: ValidationResult
    range: uriorcurie
  info:
    name: info
    description: additional information about the issue
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:resultMessage
    alias: info
    owner: ValidationResult
    range: string
class_uri: sh:ValidationResult

```
</details>