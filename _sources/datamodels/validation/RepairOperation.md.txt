

# Class: RepairOperation


_The result of performing an individual repair_





URI: [vm:RepairOperation](https://w3id.org/linkml/validation-model/RepairOperation)






```{mermaid}
 classDiagram
    class RepairOperation
    click RepairOperation href "../RepairOperation"
      Result <|-- RepairOperation
        click Result href "../Result"
      
      RepairOperation : info
        
      RepairOperation : modified
        
      RepairOperation : repairs
        
          
    
    
    RepairOperation --> "0..1" ValidationResult : repairs
    click ValidationResult href "../ValidationResult"

        
      RepairOperation : successful
        
      
```





## Inheritance
* [Result](Result.md)
    * **RepairOperation**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [repairs](repairs.md) | 0..1 <br/> [ValidationResult](ValidationResult.md) |  | direct |
| [modified](modified.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [successful](successful.md) | 0..1 <br/> [Boolean](Boolean.md) |  | direct |
| [info](info.md) | 0..1 <br/> [String](String.md) |  | direct |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [RepairReport](RepairReport.md) | [results](results.md) | range | [RepairOperation](RepairOperation.md) |






## TODOs

* integrate with kgcl data model, to be able to describe changes

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:RepairOperation |
| native | vm:RepairOperation |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RepairOperation
description: The result of performing an individual repair
todos:
- integrate with kgcl data model, to be able to describe changes
from_schema: https://w3id.org/linkml/validation_results
is_a: Result
attributes:
  repairs:
    name: repairs
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - RepairOperation
    range: ValidationResult
  modified:
    name: modified
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - RepairOperation
    range: boolean
  successful:
    name: successful
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    domain_of:
    - RepairOperation
    range: boolean
  info:
    name: info
    from_schema: https://w3id.org/linkml/validation_results
    domain_of:
    - ValidationResult
    - MappingValidationResult
    - RepairOperation
    range: string

```
</details>

### Induced

<details>
```yaml
name: RepairOperation
description: The result of performing an individual repair
todos:
- integrate with kgcl data model, to be able to describe changes
from_schema: https://w3id.org/linkml/validation_results
is_a: Result
attributes:
  repairs:
    name: repairs
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: repairs
    owner: RepairOperation
    domain_of:
    - RepairOperation
    range: ValidationResult
  modified:
    name: modified
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: modified
    owner: RepairOperation
    domain_of:
    - RepairOperation
    range: boolean
  successful:
    name: successful
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    alias: successful
    owner: RepairOperation
    domain_of:
    - RepairOperation
    range: boolean
  info:
    name: info
    from_schema: https://w3id.org/linkml/validation_results
    alias: info
    owner: RepairOperation
    domain_of:
    - ValidationResult
    - MappingValidationResult
    - RepairOperation
    range: string

```
</details>