

# Slot: subject_match_field_one_of


_The field in the subject to be matched. Multiple values can be provided, it must match at least one._





URI: [mappingrules:subject_match_field_one_of](https://w3id.org/oak/mapping-rules-datamodel/subject_match_field_one_of)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Precondition](Precondition.md) | A pattern to be matched against an individual SSSOM mapping |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://w3id.org/oak/mapping-rules-datamodel




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | mappingrules:subject_match_field_one_of |
| native | mappingrules:subject_match_field_one_of |




## LinkML Source

<details>
```yaml
name: subject_match_field_one_of
description: The field in the subject to be matched. Multiple values can be provided,
  it must match at least one.
from_schema: https://w3id.org/oak/mapping-rules-datamodel
rank: 1000
alias: subject_match_field_one_of
owner: Precondition
domain_of:
- Precondition
range: string
multivalued: true

```
</details>