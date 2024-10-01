

# Class: DefinitionValidationResult



URI: [vm:DefinitionValidationResult](https://w3id.org/linkml/validation-model/DefinitionValidationResult)






```{mermaid}
 classDiagram
    class DefinitionValidationResult
    click DefinitionValidationResult href "../DefinitionValidationResult"
      ValidationResult <|-- DefinitionValidationResult
        click ValidationResult href "../ValidationResult"
      
      DefinitionValidationResult : definition
        
      DefinitionValidationResult : definition_source
        
      DefinitionValidationResult : info
        
      DefinitionValidationResult : instantiates
        
          
    
    
    DefinitionValidationResult --> "0..1" Node : instantiates
    click Node href "../Node"

        
      DefinitionValidationResult : object
        
          
    
    
    DefinitionValidationResult --> "0..1" Node : object
    click Node href "../Node"

        
      DefinitionValidationResult : object_str
        
      DefinitionValidationResult : predicate
        
          
    
    
    DefinitionValidationResult --> "0..1" Node : predicate
    click Node href "../Node"

        
      DefinitionValidationResult : proposed_new_definition
        
      DefinitionValidationResult : severity
        
          
    
    
    DefinitionValidationResult --> "0..1" SeverityOptions : severity
    click SeverityOptions href "../SeverityOptions"

        
      DefinitionValidationResult : source
        
      DefinitionValidationResult : subject
        
          
    
    
    DefinitionValidationResult --> "1" Node : subject
    click Node href "../Node"

        
      DefinitionValidationResult : type
        
          
    
    
    DefinitionValidationResult --> "1" ConstraintComponent : type
    click ConstraintComponent href "../ConstraintComponent"

        
      
```





## Inheritance
* [Result](Result.md)
    * [ValidationResult](ValidationResult.md)
        * **DefinitionValidationResult**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [definition](definition.md) | 0..1 <br/> [String](String.md) |  | direct |
| [definition_source](definition_source.md) | 0..1 <br/> [String](String.md) |  | direct |
| [proposed_new_definition](proposed_new_definition.md) | 0..1 <br/> [String](String.md) |  | direct |
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
| self | vm:DefinitionValidationResult |
| native | vm:DefinitionValidationResult |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DefinitionValidationResult
from_schema: https://w3id.org/linkml/validation_results
is_a: ValidationResult
attributes:
  definition:
    name: definition
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - DefinitionValidationResult
    range: string
  definition_source:
    name: definition_source
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - DefinitionValidationResult
    range: string
  proposed_new_definition:
    name: proposed_new_definition
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - DefinitionValidationResult
    range: string

```
</details>

### Induced

<details>
```yaml
name: DefinitionValidationResult
from_schema: https://w3id.org/linkml/validation_results
is_a: ValidationResult
attributes:
  definition:
    name: definition
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: definition
    owner: DefinitionValidationResult
    domain_of:
    - DefinitionValidationResult
    range: string
  definition_source:
    name: definition_source
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: definition_source
    owner: DefinitionValidationResult
    domain_of:
    - DefinitionValidationResult
    range: string
  proposed_new_definition:
    name: proposed_new_definition
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: proposed_new_definition
    owner: DefinitionValidationResult
    domain_of:
    - DefinitionValidationResult
    range: string
  type:
    name: type
    description: The type of validation result. SHACL validation vocabulary is recommended
      for checks against a datamodel. For principle checks use the corresponding rule
      or principle, e.g. GO RULE ID, OBO Principle ID
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:sourceConstraintComponent
    alias: type
    owner: DefinitionValidationResult
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
    owner: DefinitionValidationResult
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
    owner: DefinitionValidationResult
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
    owner: DefinitionValidationResult
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
    owner: DefinitionValidationResult
    domain_of:
    - ValidationResult
    range: Node
  object:
    name: object
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:value
    alias: object
    owner: DefinitionValidationResult
    domain_of:
    - ValidationResult
    range: Node
  object_str:
    name: object_str
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: object_str
    owner: DefinitionValidationResult
    domain_of:
    - ValidationResult
    range: string
  source:
    name: source
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: source
    owner: DefinitionValidationResult
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
    owner: DefinitionValidationResult
    domain_of:
    - ValidationResult
    - MappingValidationResult
    - RepairOperation
    range: string

```
</details>