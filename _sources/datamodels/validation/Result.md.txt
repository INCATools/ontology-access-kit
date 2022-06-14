# Class: Result
_Abstract base class for any individual report result_



* __NOTE__: this is an abstract class and should not be instantiated directly



URI: [vm:Result](https://w3id.org/linkml/validation-model/Result)




```{mermaid}
 classDiagram
      Result <|-- ValidationResult
      Result <|-- RepairOperation
      
      
```





## Inheritance
* **Result**
    * [ValidationResult](ValidationResult.md)
    * [RepairOperation](RepairOperation.md)



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Report](Report.md) | [results](results.md) | range | Result |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['vm:Result'] |
| native | ['vm:Result'] |


## LinkML Specification

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