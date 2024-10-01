

# Slot: type_severity_map


_Allows overriding of severity of a particular type_





URI: [vm:type_severity_map](https://w3id.org/linkml/validation-model/type_severity_map)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ValidationConfiguration](ValidationConfiguration.md) | Configuration parameters for execution of a validation report |  no  |







## Properties

* Range: [TypeSeverityKeyValue](TypeSeverityKeyValue.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:type_severity_map |
| native | vm:type_severity_map |




## LinkML Source

<details>
```yaml
name: type_severity_map
description: Allows overriding of severity of a particular type
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
alias: type_severity_map
owner: ValidationConfiguration
domain_of:
- ValidationConfiguration
range: TypeSeverityKeyValue
multivalued: true
inlined: true

```
</details>