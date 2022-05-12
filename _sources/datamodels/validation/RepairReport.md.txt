# Class: RepairReport
_A repair object_





URI: [reporting:RepairReport](https://w3id.org/linkml/validation-model/RepairReport)




## Inheritance

* [Report](Report.md)
    * **RepairReport**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [results](results.md) | [RepairOperation](RepairOperation.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RepairReport
description: A repair object
from_schema: https://w3id.org/linkml/validation_results
is_a: Report
slot_usage:
  results:
    name: results
    range: RepairOperation

```
</details>

### Induced

<details>
```yaml
name: RepairReport
description: A repair object
from_schema: https://w3id.org/linkml/validation_results
is_a: Report
slot_usage:
  results:
    name: results
    range: RepairOperation
attributes:
  results:
    name: results
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:result
    multivalued: true
    alias: results
    owner: RepairReport
    range: RepairOperation

```
</details>