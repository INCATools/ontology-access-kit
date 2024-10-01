

# Class: ExternalReferenceValidationResult


_A validation result where the check is to determine if a link to an external resource is still valid_





URI: [vm:ExternalReferenceValidationResult](https://w3id.org/linkml/validation-model/ExternalReferenceValidationResult)






```{mermaid}
 classDiagram
    class ExternalReferenceValidationResult
    click ExternalReferenceValidationResult href "../ExternalReferenceValidationResult"
      ValidationResult <|-- ExternalReferenceValidationResult
        click ValidationResult href "../ValidationResult"
      
      ExternalReferenceValidationResult : http_response_code
        
      ExternalReferenceValidationResult : info
        
      ExternalReferenceValidationResult : instantiates
        
          
    
    
    ExternalReferenceValidationResult --> "0..1" Node : instantiates
    click Node href "../Node"

        
      ExternalReferenceValidationResult : number_of_attempts
        
      ExternalReferenceValidationResult : object
        
          
    
    
    ExternalReferenceValidationResult --> "0..1" Node : object
    click Node href "../Node"

        
      ExternalReferenceValidationResult : object_str
        
      ExternalReferenceValidationResult : predicate
        
          
    
    
    ExternalReferenceValidationResult --> "0..1" Node : predicate
    click Node href "../Node"

        
      ExternalReferenceValidationResult : severity
        
          
    
    
    ExternalReferenceValidationResult --> "0..1" SeverityOptions : severity
    click SeverityOptions href "../SeverityOptions"

        
      ExternalReferenceValidationResult : source
        
      ExternalReferenceValidationResult : subject
        
          
    
    
    ExternalReferenceValidationResult --> "1" Node : subject
    click Node href "../Node"

        
      ExternalReferenceValidationResult : time_checked
        
      ExternalReferenceValidationResult : type
        
          
    
    
    ExternalReferenceValidationResult --> "1" ConstraintComponent : type
    click ConstraintComponent href "../ConstraintComponent"

        
      ExternalReferenceValidationResult : url
        
      
```





## Inheritance
* [Result](Result.md)
    * [ValidationResult](ValidationResult.md)
        * **ExternalReferenceValidationResult**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [url](url.md) | 0..1 <br/> [String](String.md) |  | direct |
| [time_checked](time_checked.md) | 0..1 <br/> [String](String.md) |  | direct |
| [number_of_attempts](number_of_attempts.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |
| [http_response_code](http_response_code.md) | 0..1 <br/> [Integer](Integer.md) |  | direct |
| [type](type.md) | 1 <br/> [ConstraintComponent](ConstraintComponent.md) | The type of validation result | [ValidationResult](ValidationResult.md) |
| [severity](severity.md) | 0..1 <br/> [SeverityOptions](SeverityOptions.md) | the severity of the issue | [ValidationResult](ValidationResult.md) |
| [subject](subject.md) | 1 <br/> [Node](Node.md) | The instance which the result is about | [ValidationResult](ValidationResult.md) |
| [instantiates](instantiates.md) | 0..1 <br/> [Node](Node.md) | The type of the subject | [ValidationResult](ValidationResult.md) |
| [predicate](predicate.md) | 0..1 <br/> [Node](Node.md) | The predicate or property of the subject which the result is about | [ValidationResult](ValidationResult.md) |
| [object](object.md) | 0..1 <br/> [Node](Node.md) |  | [ValidationResult](ValidationResult.md) |
| [object_str](object_str.md) | 0..1 <br/> [String](String.md) |  | [ValidationResult](ValidationResult.md) |
| [source](source.md) | 0..1 <br/> [String](String.md) |  | [ValidationResult](ValidationResult.md) |
| [info](info.md) | 0..1 <br/> [String](String.md) | additional information about the issue | [ValidationResult](ValidationResult.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:ExternalReferenceValidationResult |
| native | vm:ExternalReferenceValidationResult |







## LinkML Source

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
    rank: 1000
    domain_of:
    - ExternalReferenceValidationResult
  time_checked:
    name: time_checked
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - ExternalReferenceValidationResult
  number_of_attempts:
    name: number_of_attempts
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - ExternalReferenceValidationResult
    range: integer
  http_response_code:
    name: http_response_code
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - ExternalReferenceValidationResult
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
    rank: 1000
    alias: url
    owner: ExternalReferenceValidationResult
    domain_of:
    - ExternalReferenceValidationResult
    range: string
  time_checked:
    name: time_checked
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: time_checked
    owner: ExternalReferenceValidationResult
    domain_of:
    - ExternalReferenceValidationResult
    range: string
  number_of_attempts:
    name: number_of_attempts
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: number_of_attempts
    owner: ExternalReferenceValidationResult
    domain_of:
    - ExternalReferenceValidationResult
    range: integer
  http_response_code:
    name: http_response_code
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: http_response_code
    owner: ExternalReferenceValidationResult
    domain_of:
    - ExternalReferenceValidationResult
    range: integer
  type:
    name: type
    description: The type of validation result. SHACL validation vocabulary is recommended
      for checks against a datamodel. For principle checks use the corresponding rule
      or principle, e.g. GO RULE ID, OBO Principle ID
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:sourceConstraintComponent
    alias: type
    owner: ExternalReferenceValidationResult
    domain_of:
    - TypeSeverityKeyValue
    - ValidationResult
    range: ConstraintComponent
    required: true
  severity:
    name: severity
    description: the severity of the issue
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:resultSeverity
    alias: severity
    owner: ExternalReferenceValidationResult
    domain_of:
    - TypeSeverityKeyValue
    - ValidationResult
    range: severity_options
  subject:
    name: subject
    description: The instance which the result is about
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:focusNode
    alias: subject
    owner: ExternalReferenceValidationResult
    domain_of:
    - ValidationResult
    range: Node
    required: true
  instantiates:
    name: instantiates
    description: The type of the subject
    from_schema: https://w3id.org/linkml/validation_results
    exact_mappings:
    - sh:sourceShape
    rank: 1000
    alias: instantiates
    owner: ExternalReferenceValidationResult
    domain_of:
    - ValidationResult
    range: Node
  predicate:
    name: predicate
    description: The predicate or property of the subject which the result is about
    from_schema: https://w3id.org/linkml/validation_results
    related_mappings:
    - sh:resultPath
    rank: 1000
    alias: predicate
    owner: ExternalReferenceValidationResult
    domain_of:
    - ValidationResult
    range: Node
  object:
    name: object
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:value
    alias: object
    owner: ExternalReferenceValidationResult
    domain_of:
    - ValidationResult
    range: Node
  object_str:
    name: object_str
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: object_str
    owner: ExternalReferenceValidationResult
    domain_of:
    - ValidationResult
    range: string
  source:
    name: source
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: source
    owner: ExternalReferenceValidationResult
    domain_of:
    - ValidationResult
    range: string
  info:
    name: info
    description: additional information about the issue
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:resultMessage
    alias: info
    owner: ExternalReferenceValidationResult
    domain_of:
    - ValidationResult
    - MappingValidationResult
    - RepairOperation
    range: string

```
</details>