

# Slot: max_number_results_per_type


_if set then truncate results such that no more than this number of results are reported per type_





URI: [vm:max_number_results_per_type](https://w3id.org/linkml/validation-model/max_number_results_per_type)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ValidationConfiguration](ValidationConfiguration.md) | Configuration parameters for execution of a validation report |  no  |







## Properties

* Range: [Integer](Integer.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:max_number_results_per_type |
| native | vm:max_number_results_per_type |




## LinkML Source

<details>
```yaml
name: max_number_results_per_type
description: if set then truncate results such that no more than this number of results
  are reported per type
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
alias: max_number_results_per_type
owner: ValidationConfiguration
domain_of:
- ValidationConfiguration
range: integer

```
</details>