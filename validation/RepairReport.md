# Class: RepairReport
_A report that consists of repair operation results_





URI: [vm:RepairReport](https://w3id.org/linkml/validation-model/RepairReport)




```{mermaid}
 classDiagram
      Report <|-- RepairReport
      
      RepairReport : results
      

```





## Inheritance
* [Report](Report.md)
    * **RepairReport**



## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [results](results.md) | [RepairOperation](RepairOperation.md) | 0..* | collection of results  | . |


## Usages



## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results







## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | ['vm:RepairReport'] |
| native | ['vm:RepairReport'] |


## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: RepairReport
description: A report that consists of repair operation results
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
description: A report that consists of repair operation results
from_schema: https://w3id.org/linkml/validation_results
is_a: Report
slot_usage:
  results:
    name: results
    range: RepairOperation
attributes:
  results:
    name: results
    description: collection of results
    from_schema: https://w3id.org/linkml/validation_results
    slot_uri: sh:result
    multivalued: true
    alias: results
    owner: RepairReport
    range: RepairOperation
    inlined: true
    inlined_as_list: true

```
</details>