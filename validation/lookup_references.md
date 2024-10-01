

# Slot: lookup_references


_if true, then look up references used as provenance (axiom annotation). This may include looking up the PMID and checking if a publication is retracted._





URI: [vm:lookup_references](https://w3id.org/linkml/validation-model/lookup_references)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ValidationConfiguration](ValidationConfiguration.md) | Configuration parameters for execution of a validation report |  no  |







## Properties

* Range: [Boolean](Boolean.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/linkml/validation_results




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | vm:lookup_references |
| native | vm:lookup_references |




## LinkML Source

<details>
```yaml
name: lookup_references
description: if true, then look up references used as provenance (axiom annotation).
  This may include looking up the PMID and checking if a publication is retracted.
from_schema: https://w3id.org/linkml/validation_results
rank: 1000
alias: lookup_references
owner: ValidationConfiguration
domain_of:
- ValidationConfiguration
range: boolean

```
</details>