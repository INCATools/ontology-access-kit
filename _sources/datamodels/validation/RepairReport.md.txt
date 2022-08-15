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

| Name | Cardinality and Range  | Description  |
| ---  | ---  | --- |
| [results](results.md) | 0..* <br/> [RepairOperation](RepairOperation.md)  | collection of results  |


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
rank: 1000
is_a: Report
slot_usage:
  results:
    name: results
    domain_of:
    - Report
    - Report
    range: RepairOperation

```
</details>

### Induced

<details>
```yaml
name: RepairReport
description: A report that consists of repair operation results
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
is_a: Report
slot_usage:
  results:
    name: results
    domain_of:
    - Report
    - Report
    range: RepairOperation
attributes:
  results:
    name: results
    description: collection of results
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:result
    multivalued: true
    alias: results
    owner: RepairReport
    domain_of:
    - Report
    - Report
    range: RepairOperation
    inlined: true
    inlined_as_list: true

```
</details>