

# Class: ValidationResult


_An individual result arising from validation of a data instance using a particular rule_





URI: [sh:ValidationResult](http://www.w3.org/ns/shacl#ValidationResult)






```{mermaid}
 classDiagram
    class ValidationResult
    click ValidationResult href "../ValidationResult"
      Result <|-- ValidationResult
        click Result href "../Result"
      

      ValidationResult <|-- DefinitionValidationResult
        click DefinitionValidationResult href "../DefinitionValidationResult"
      ValidationResult <|-- ExternalReferenceValidationResult
        click ExternalReferenceValidationResult href "../ExternalReferenceValidationResult"
      
      
      ValidationResult : info
        
      ValidationResult : instantiates
        
          
    
    
    ValidationResult --> "0..1" Node : instantiates
    click Node href "../Node"

        
      ValidationResult : object
        
          
    
    
    ValidationResult --> "0..1" Node : object
    click Node href "../Node"

        
      ValidationResult : object_str
        
      ValidationResult : predicate
        
          
    
    
    ValidationResult --> "0..1" Node : predicate
    click Node href "../Node"

        
      ValidationResult : severity
        
          
    
    
    ValidationResult --> "0..1" SeverityOptions : severity
    click SeverityOptions href "../SeverityOptions"

        
      ValidationResult : source
        
      ValidationResult : subject
        
          
    
    
    ValidationResult --> "1" Node : subject
    click Node href "../Node"

        
      ValidationResult : type
        
          
    
    
    ValidationResult --> "1" ConstraintComponent : type
    click ConstraintComponent href "../ConstraintComponent"

        
      
```





## Inheritance
* [Result](Result.md)
    * **ValidationResult**
        * [DefinitionValidationResult](DefinitionValidationResult.md)
        * [ExternalReferenceValidationResult](ExternalReferenceValidationResult.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [type](type.md) | 1 <br/> [ConstraintComponent](ConstraintComponent.md) | The type of validation result | direct |
| [severity](severity.md) | 0..1 <br/> [SeverityOptions](SeverityOptions.md) | the severity of the issue | direct |
| [subject](subject.md) | 1 <br/> [Node](Node.md) | The instance which the result is about | direct |
| [instantiates](instantiates.md) | 0..1 <br/> [Node](Node.md) | The type of the subject | direct |
| [predicate](predicate.md) | 0..1 <br/> [Node](Node.md) | The predicate or property of the subject which the result is about | direct |
| [object](object.md) | 0..1 <br/> [Node](Node.md) |  | direct |
| [object_str](object_str.md) | 0..1 <br/> [String](String.md) |  | direct |
| [source](source.md) | 0..1 <br/> [String](String.md) |  | direct |
| [info](info.md) | 0..1 <br/> [String](String.md) | additional information about the issue | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ValidationReport](ValidationReport.md) | [results](results.md) | range | [ValidationResult](ValidationResult.md) |
| [RepairOperation](RepairOperation.md) | [repairs](repairs.md) | range | [ValidationResult](ValidationResult.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:ValidationResult |
| native | vm:ValidationResult |







## LinkML Source

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
    rank: 1000
    slot_uri: sh:sourceConstraintComponent
    alias: type
    owner: ValidationResult
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
    owner: ValidationResult
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
    owner: ValidationResult
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
    owner: ValidationResult
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
    owner: ValidationResult
    domain_of:
    - ValidationResult
    range: Node
  object:
    name: object
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:value
    alias: object
    owner: ValidationResult
    domain_of:
    - ValidationResult
    range: Node
  object_str:
    name: object_str
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: object_str
    owner: ValidationResult
    domain_of:
    - ValidationResult
    range: string
  source:
    name: source
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: source
    owner: ValidationResult
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
    owner: ValidationResult
    domain_of:
    - ValidationResult
    - MappingValidationResult
    - RepairOperation
    range: string
class_uri: sh:ValidationResult

```
</details>