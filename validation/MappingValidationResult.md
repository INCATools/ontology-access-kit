

# Class: MappingValidationResult


_A validation result where the check is to determine if a mapping is correct_





URI: [vm:MappingValidationResult](https://w3id.org/linkml/validation-model/MappingValidationResult)






```{mermaid}
 classDiagram
    class MappingValidationResult
    click MappingValidationResult href "../MappingValidationResult"
      Result <|-- MappingValidationResult
        click Result href "../Result"
      
      MappingValidationResult : category
        
      MappingValidationResult : confidence
        
      MappingValidationResult : info
        
      MappingValidationResult : object_id
        
      MappingValidationResult : object_info
        
      MappingValidationResult : predicate_id
        
      MappingValidationResult : problem
        
      MappingValidationResult : subject_id
        
      MappingValidationResult : subject_info
        
      MappingValidationResult : suggested_modifications
        
      MappingValidationResult : suggested_predicate
        
      
```





## Inheritance
* [Result](Result.md)
    * **MappingValidationResult**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [subject_id](subject_id.md) | 0..1 <br/> [String](String.md) |  | direct |
| [subject_info](subject_info.md) | 0..1 <br/> [String](String.md) |  | direct |
| [object_id](object_id.md) | 0..1 <br/> [String](String.md) |  | direct |
| [object_info](object_info.md) | 0..1 <br/> [String](String.md) |  | direct |
| [predicate_id](predicate_id.md) | 0..1 <br/> [String](String.md) |  | direct |
| [category](category.md) | 0..1 <br/> [String](String.md) | The category of the validation issue | direct |
| [problem](problem.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [info](info.md) | 0..1 <br/> [String](String.md) |  | direct |
| [confidence](confidence.md) | 0..1 <br/> [Float](Float.md) |  | direct |
| [suggested_predicate](suggested_predicate.md) | 0..1 <br/> [String](String.md) |  | direct |
| [suggested_modifications](suggested_modifications.md) | 0..1 <br/> [String](String.md) |  | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:MappingValidationResult |
| native | vm:MappingValidationResult |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: MappingValidationResult
description: A validation result where the check is to determine if a mapping is correct
from_schema: https://w3id.org/linkml/validation_results
is_a: Result
attributes:
  subject_id:
    name: subject_id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: string
  subject_info:
    name: subject_info
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: string
  object_id:
    name: object_id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: string
  object_info:
    name: object_info
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: string
  predicate_id:
    name: predicate_id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: string
  category:
    name: category
    description: The category of the validation issue
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: string
  problem:
    name: problem
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: boolean
  info:
    name: info
    from_schema: https://w3id.org/linkml/validation_results
    domain_of:
    - ValidationResult
    - MappingValidationResult
    - RepairOperation
    range: string
  confidence:
    name: confidence
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: float
  suggested_predicate:
    name: suggested_predicate
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: string
  suggested_modifications:
    name: suggested_modifications
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - MappingValidationResult
    range: string

```
</details>

### Induced

<details>
```yaml
name: MappingValidationResult
description: A validation result where the check is to determine if a mapping is correct
from_schema: https://w3id.org/linkml/validation_results
is_a: Result
attributes:
  subject_id:
    name: subject_id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: subject_id
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: string
  subject_info:
    name: subject_info
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: subject_info
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: string
  object_id:
    name: object_id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: object_id
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: string
  object_info:
    name: object_info
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: object_info
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: string
  predicate_id:
    name: predicate_id
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: predicate_id
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: string
  category:
    name: category
    description: The category of the validation issue
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: category
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: string
  problem:
    name: problem
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: problem
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: boolean
  info:
    name: info
    from_schema: https://w3id.org/linkml/validation_results
    alias: info
    owner: MappingValidationResult
    domain_of:
    - ValidationResult
    - MappingValidationResult
    - RepairOperation
    range: string
  confidence:
    name: confidence
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: confidence
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: float
  suggested_predicate:
    name: suggested_predicate
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: suggested_predicate
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: string
  suggested_modifications:
    name: suggested_modifications
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: suggested_modifications
    owner: MappingValidationResult
    domain_of:
    - MappingValidationResult
    range: string

```
</details>