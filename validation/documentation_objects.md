

# Slot: documentation_objects


_paths or URLs to files containing best practice documentation, SOPs, etc. Primarily for AI agents to read when performing validation._





URI: [vm:documentation_objects](https://w3id.org/linkml/validation-model/documentation_objects)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ValidationConfiguration](ValidationConfiguration.md) | Configuration parameters for execution of a validation report |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:documentation_objects |
| native | vm:documentation_objects |




## LinkML Source

<details>
```yaml
name: documentation_objects
description: paths or URLs to files containing best practice documentation, SOPs,
  etc. Primarily for AI agents to read when performing validation.
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
alias: documentation_objects
owner: ValidationConfiguration
domain_of:
- ValidationConfiguration
range: string
multivalued: true

```
</details>