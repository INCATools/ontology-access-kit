# Class: Report


_A report object that is a holder to multiple report results_




* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [vm:Report](https://w3id.org/linkml/validation-model/Report)




```{mermaid}
 classDiagram
    class Report
      Report <|-- ValidationReport
      Report <|-- RepairReport
      
      Report : results
        
          Report --> Result : results
        
      
```





## Inheritance
* **Report**
    * [ValidationReport](ValidationReport.md)
    * [RepairReport](RepairReport.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [results](results.md) | 0..* <br/> [Result](Result.md) | collection of results | direct |









## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:Report |
| native | vm:Report |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Report
description: A report object that is a holder to multiple report results
from_schema: https://w3id.org/linkml/validation_results
abstract: true
slots:
- results

```
</details>

### Induced

<details>
```yaml
name: Report
description: A report object that is a holder to multiple report results
from_schema: https://w3id.org/linkml/validation_results
abstract: true
attributes:
  results:
    name: results
    description: collection of results
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:result
    multivalued: true
    alias: results
    owner: Report
    domain_of:
    - Report
    range: Result
    inlined: true
    inlined_as_list: true

```
</details>