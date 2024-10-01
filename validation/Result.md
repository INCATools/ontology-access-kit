

# Class: Result


_Abstract base class for any individual report result_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [vm:Result](https://w3id.org/linkml/validation-model/Result)






```{mermaid}
 classDiagram
    class Result
    click Result href "../Result"
      Result <|-- ValidationResult
        click ValidationResult href "../ValidationResult"
      Result <|-- MappingValidationResult
        click MappingValidationResult href "../MappingValidationResult"
      Result <|-- RepairOperation
        click RepairOperation href "../RepairOperation"
      
      
```





## Inheritance
* **Result**
    * [ValidationResult](ValidationResult.md)
    * [MappingValidationResult](MappingValidationResult.md)
    * [RepairOperation](RepairOperation.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Report](Report.md) | [results](results.md) | range | [Result](Result.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:Result |
| native | vm:Result |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Result
description: Abstract base class for any individual report result
from_schema: https://w3id.org/linkml/validation_results
abstract: true

```
</details>

### Induced

<details>
```yaml
name: Result
description: Abstract base class for any individual report result
from_schema: https://w3id.org/linkml/validation_results
abstract: true

```
</details>