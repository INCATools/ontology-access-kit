

# Class: ValidationReport


_A report that consists of validation results_





URI: [sh:ValidationReport](http://www.w3.org/ns/shacl#ValidationReport)






```{mermaid}
 classDiagram
    class ValidationReport
    click ValidationReport href "../ValidationReport"
      Report <|-- ValidationReport
        click Report href "../Report"
      
      ValidationReport : results
        
          
    
    
    ValidationReport --> "*" ValidationResult : results
    click ValidationResult href "../ValidationResult"

        
      
```





## Inheritance
* [Report](Report.md)
    * **ValidationReport**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [results](results.md) | * <br/> [ValidationResult](ValidationResult.md) | collection of results | [Report](Report.md) |









## TODOs

* add prov object

## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:ValidationReport |
| native | vm:ValidationReport |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ValidationReport
description: A report that consists of validation results
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
description: A report that consists of validation results
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
    description: collection of results
    from_schema: https://w3id.org/linkml/validation_results
    rank: 1000
    slot_uri: sh:result
    alias: results
    owner: ValidationReport
    domain_of:
    - Report
    range: ValidationResult
    multivalued: true
    inlined: true
    inlined_as_list: true
class_uri: sh:ValidationReport

```
</details>