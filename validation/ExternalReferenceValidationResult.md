# Class: ExternalReferenceValidationResult
_A validation result where the check is to determine if a link to an external resource is still valid_





URI: [vm:ExternalReferenceValidationResult](https://w3id.org/linkml/validation-model/ExternalReferenceValidationResult)




```{mermaid}
 classDiagram
      ValidationResult <|-- ExternalReferenceValidationResult
      
      ExternalReferenceValidationResult : http_response_code
      ExternalReferenceValidationResult : info
      ExternalReferenceValidationResult : instantiates
      ExternalReferenceValidationResult : number_of_attempts
      ExternalReferenceValidationResult : object
      ExternalReferenceValidationResult : object_str
      ExternalReferenceValidationResult : predicate
      ExternalReferenceValidationResult : severity
      ExternalReferenceValidationResult : source
      ExternalReferenceValidationResult : subject
      ExternalReferenceValidationResult : time_checked
      ExternalReferenceValidationResult : type
      ExternalReferenceValidationResult : url
      

```





## Inheritance
* [Result](Result.md)
    * [ValidationResult](ValidationResult.md)
        * **ExternalReferenceValidationResult**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [url](url.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [time_checked](time_checked.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |
| [number_of_attempts](number_of_attempts.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
| [http_response_code](http_response_code.md) | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) | 0..1 | None  | . |
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



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['vm:ExternalReferenceValidationResult'] |
| native | ['vm:ExternalReferenceValidationResult'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ExternalReferenceValidationResult
description: A validation result where the check is to determine if a link to an external
  resource is still valid
from_schema: https://w3id.org/linkml/validation_results
is_a: ValidationResult
attributes:
  url:
    name: url
    from_schema: https://w3id.org/linkml/validation_results
  time_checked:
    name: time_checked
    from_schema: https://w3id.org/linkml/validation_results
  number_of_attempts:
    name: number_of_attempts
    from_schema: https://w3id.org/linkml/validation_results
    range: integer
  http_response_code:
    name: http_response_code
    from_schema: https://w3id.org/linkml/validation_results
    range: integer

```
</details>

### Induced

<details>
```yaml
name: ExternalReferenceValidationResult
description: A validation result where the check is to determine if a link to an external
  resource is still valid
from_schema: https://w3id.org/linkml/validation_results
is_a: ValidationResult
attributes:
  url:
    name: url
    from_schema: https://w3id.org/linkml/validation_results
    alias: url
    owner: ExternalReferenceValidationResult
    range: string
  time_checked:
    name: time_checked
    from_schema: https://w3id.org/linkml/validation_results
    alias: time_checked
    owner: ExternalReferenceValidationResult
    range: string
  number_of_attempts:
    name: number_of_attempts
    from_schema: https://w3id.org/linkml/validation_results
    alias: number_of_attempts
    owner: ExternalReferenceValidationResult
    range: integer
  http_response_code:
    name: http_response_code
    from_schema: https://w3id.org/linkml/validation_results
    alias: http_response_code
    owner: ExternalReferenceValidationResult
    range: integer
  type:
    name: type
    description: The type of validation result. SHACL validation vocabulary is recommended
      for checks against a datamodel. For principle checks use the corresponding rule
      or principle, e.g. GO RULE ID, OBO Principle ID
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:sourceConstraintComponent
    alias: type
    owner: ExternalReferenceValidationResult
    range: uriorcurie
    required: true
  severity:
    name: severity
    description: the severity of the issue
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:resultSeverity
    alias: severity
    owner: ExternalReferenceValidationResult
    range: severity_options
  subject:
    name: subject
    description: The instance which the result is about
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:focusNode
    alias: subject
    owner: ExternalReferenceValidationResult
    range: uriorcurie
    required: true
  instantiates:
    name: instantiates
    description: The type of the subject
    from_schema: https://w3id.org/linkml/validation_results
    exact_mappings:
    - sh:sourceShape
    alias: instantiates
    owner: ExternalReferenceValidationResult
    range: uriorcurie
  predicate:
    name: predicate
    description: The predicate or property of the subject which the result is about
    from_schema: https://w3id.org/linkml/validation_results
    related_mappings:
    - sh:resultPath
    alias: predicate
    owner: ExternalReferenceValidationResult
    range: uriorcurie
  object:
    name: object
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:value
    alias: object
    owner: ExternalReferenceValidationResult
    range: uriorcurie
  object_str:
    name: object_str
    from_schema: https://w3id.org/linkml/validation_results
    alias: object_str
    owner: ExternalReferenceValidationResult
    range: string
  source:
    name: source
    from_schema: https://w3id.org/linkml/validation_results
    alias: source
    owner: ExternalReferenceValidationResult
    range: uriorcurie
  info:
    name: info
    description: additional information about the issue
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:resultMessage
    alias: info
    owner: ExternalReferenceValidationResult
    range: string

```
</details>