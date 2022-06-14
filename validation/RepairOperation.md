# Class: RepairOperation
_The result of performing an individual repair_





URI: [vm:RepairOperation](https://w3id.org/linkml/validation-model/RepairOperation)




```{mermaid}
 classDiagram
      Result <|-- RepairOperation
      
      RepairOperation : info
      RepairOperation : modified
      RepairOperation : repairs
      RepairOperation : successful
      

```





## Inheritance
* [Result](Result.md)
    * **RepairOperation**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [repairs](repairs.md) | [ValidationResult](ValidationResult.md) | 0..1 | None  | . |
| [modified](modified.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [successful](successful.md) | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) | 0..1 | None  | . |
| [info](info.md) | [xsd:string](http://www.w3.org/2001/XMLSchema#string) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [RepairReport](RepairReport.md) | [results](results.md) | range | RepairOperation |



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['vm:RepairOperation'] |
| native | ['vm:RepairOperation'] |


## LinkML Specification

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
    range: ValidationResult
  modified:
    name: modified
    from_schema: https://w3id.org/linkml/validation_results
    range: boolean
  successful:
    name: successful
    from_schema: https://w3id.org/linkml/validation_results
    range: boolean
  info:
    name: info
    from_schema: https://w3id.org/linkml/validation_results
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
    alias: repairs
    owner: RepairOperation
    range: ValidationResult
  modified:
    name: modified
    from_schema: https://w3id.org/linkml/validation_results
    alias: modified
    owner: RepairOperation
    range: boolean
  successful:
    name: successful
    from_schema: https://w3id.org/linkml/validation_results
    alias: successful
    owner: RepairOperation
    range: boolean
  info:
    name: info
    from_schema: https://w3id.org/linkml/validation_results
    alias: info
    owner: RepairOperation
    range: string

```
</details>