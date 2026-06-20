

# Slot: results


_collection of results_





URI: [sh:result](http://www.w3.org/ns/shacl#result)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Report](Report.md) | A report object that is a holder to multiple report results |  no  |
| [ValidationReport](ValidationReport.md) | A report that consists of validation results |  yes  |
| [RepairReport](RepairReport.md) | A report that consists of repair operation results |  yes  |







## Properties

* Range: [Result](Result.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | sh:result |
| native | vm:results |




## LinkML Source

<details>
```yaml
name: results
description: collection of results
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
slot_uri: sh:result
alias: results
domain_of:
- Report
range: Result
multivalued: true
inlined: true
inlined_as_list: true

```
</details>