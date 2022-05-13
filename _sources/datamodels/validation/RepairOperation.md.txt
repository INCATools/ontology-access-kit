# Class: RepairOperation




URI: [reporting:RepairOperation](https://w3id.org/linkml/validation-model/RepairOperation)




## Inheritance

* [Result](Result.md)
    * **RepairOperation**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [repairs](repairs.md) | [ValidationResult](ValidationResult.md) | 0..1 | None  | . |
| [modified](modified.md) | [boolean](boolean.md) | 0..1 | None  | . |
| [successful](successful.md) | [boolean](boolean.md) | 0..1 | None  | . |


## Usages


| used by | used in | type | used |
| ---  | --- | --- | --- |
| [RepairReport](RepairReport.md) | [results](results.md) | range | RepairOperation |



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RepairOperation
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

```
</details>

### Induced

<details>
```yaml
name: RepairOperation
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

```
</details>