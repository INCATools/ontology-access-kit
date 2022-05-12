# Class: ValidationReport
_A holder for multiple validation results_





URI: [sh:ValidationReport](http://www.w3.org/ns/shacl#ValidationReport)




## Inheritance

* [Report](Report.md)
    * **ValidationReport**




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [results](results.md) | [ValidationResult](ValidationResult.md) | 0..* | None  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ValidationReport
description: A holder for multiple validation results
todos:
- add prov object
from_schema: https://w3id.org/linkml/validation_results
is_a: Report
slot_usage:
  results:
    name: results
    range: ValidationResult
class_uri: sh:ValidationReport

```
</details>

### Induced

<details>
```yaml
name: ValidationReport
description: A holder for multiple validation results
todos:
- add prov object
from_schema: https://w3id.org/linkml/validation_results
is_a: Report
slot_usage:
  results:
    name: results
    range: ValidationResult
attributes:
  results:
    name: results
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:result
    multivalued: true
    alias: results
    owner: ValidationReport
    range: ValidationResult
class_uri: sh:ValidationReport

```
</details>