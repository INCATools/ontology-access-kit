# Class: RepairReport
_A report that consists of repair operation results_




URI: [vm:RepairReport](https://w3id.org/linkml/validation-model/RepairReport)



```{mermaid}
 classDiagram
    class RepairReport
      Report <|-- RepairReport
      
      RepairReport : results
        
          RepairReport ..> RepairOperation : results
        
      
```





## Inheritance
* [Report](Report.md)
    * **RepairReport**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [results](results.md) | 0..* <br/> [RepairOperation](RepairOperation.md) | collection of results | [Report](Report.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:RepairReport |
| native | vm:RepairReport |





## LinkML Source

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
    range: RepairOperation
    inlined: true
    inlined_as_list: true

```
</details>